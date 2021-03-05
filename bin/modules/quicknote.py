from core.helpers import FileManager, open_vim, Git, ask
from os import path, environ, listdir, remove, rename
from subprocess import call
from yamlize import Sequence, Object, Attribute


# qn class
class Qn():
    def __init__(self, data_path):
        self.data_path = path.join(data_path, 'notes')
        if self.data_path[0] == '~':
            self.data_path = path.expanduser(self.data_path)
        manifest_path = path.join(self.data_path, 'qn.manifest')

        if FileManager.directory_exists(self.data_path) == False:
            FileManager.create_directory(self.data_path)

        if FileManager.file_exists(manifest_path) == False:
            manifest = QnManifest()
            content = QnManifest.dump(manifest)
            FileManager.try_create_file(manifest_path, content)

        self.__load_manifest()

    def process_command(self, arg):
        """
        qn help

        Module for note taking.

        Commands list:
            new <note name> <-s>                | creates new note and opens it in vim. If -s argument is used vim won't be opened.
            edit <note name>                    | opens note in vim
            list <-u>                           | lists all tracked notes. If -u argument is used manifest will be updated before printing list
            delete <note name>                  | deletes note
            save                                | commits all changes and pushes them to repo. Available only if git support is turned on.
            rename <note name> <new note name>  | renames note to 'new note name'
            find <keyword>                      | prints list of all the notes containing 'keyoword' in their name
        """
        args = arg.split()
        if len(args) == 0:
            print("Please provide command. If you need help use 'help qn'")
            return
        if args[0] == 'new':
            self.__process_new_command(args)
        elif args[0] == 'edit':
            self.__process_edit_command(args)
        elif args[0] == 'list':
            self.__process_list_command(args)
        elif args[0] == 'delete':
            self.__process_delete_command(args)
        elif args[0] == 'save':
            self.__process_save_command(args)
        elif args[0] == 'rename':
            self.__process_rename_command(args)
        elif args[0] == 'find':
            self.__process_find_conmmand(args)
        else:
            print(f"Unknown command 'qn {args[0]}'")

    def __process_new_command(self, args):
        if len(args) == 1:
            print("Please provide 'note name'")
            return
        if len(args) > 3:
            print(
                f"'qn new' takes up to 2 arguments. {len(args)-1} were provided."
            )
        if len(args) == 3 and args[2] != '-s':
            print(
                f"Unknown argument {args[2]}. Only known flag argument is '-s'."
            )

        note_name = args[1]
        silent = len(args) == 3
        print(f"note: {note_name}\nsilent: {silent}")

        if FileManager.file_exists(path.join(self.data_path, note_name)):
            print(f"File {note_name}.md already exists")
            return
        if self.manifest.contains(note_name):
            print(f"File already exists in the manifest")
            return

        note_path = path.join(self.data_path, f"{note_name}.md")
        content = f"# {note_name}"
        FileManager.try_create_file(note_path, content)
        self.__add_to_manifest(note_name)
        self.__save_manifest()
        if silent == False:
            open_vim(note_path)

    def __process_edit_command(self, args):
        if len(args) == 1:
            print('Please provide name of the note you want to edit')
            return
        elif len(args) > 2:
            print(
                "'qn edit' takes only 1 argument. {len(args)-1} were provided")
            return

        note_name = args[1]
        if self.manifest.contains(note_name) == False:
            print(f"Unknown note name {note_name}")
            return

        print(f"note name: {note_name}")
        note_path = path.join(self.data_path, f"{note_name}.md")
        open_vim(note_path)

    def __process_list_command(self, args):
        if len(args) > 2:
            print(
                f"'qn list takes only 1 argument. {len(args)-1} were provided."
            )
            return
        if len(args) == 2 and args[1] != '-u':
            print(f"Unknown argument {args[1]}")
            return

        if len(args) == 2 and args[1] == '-u':
            self.__update_manifest_file()

        for n in self.manifest:
            print(n.name)

    def __process_delete_command(self, args):
        if len(args) == 1:
            print('Please provide note name to be deleted.')
            return
        elif len(args) > 2:
            print(
                f"'qn delete` takes one argument. {len(args)-1} were provided."
            )
            return

        note_name = args[1]
        if self.manifest.contains(note_name) == False:
            print(f"Unknown note {note_name}")

        self.__remove_note_from_manifest(note_name)
        note_path = path.join(self.data_path, f"{note_name}.md")
        FileManager.delete_file(note_path)
        print(f"Note {note_name} was deleted")

    def __process_save_command(self, args):
        if len(args) > 2:
            print(f"'qn save' doen't take any arguments.")
            return

        status = Git.status(self.data_path)
        if status == 'fatal':
            print("'qn' data folder isn't part of git repository")
            return
        Git.add_all(self.data_path)
        Git.commit(self.data_path)
        while True:
            decision = ask(
                "Do you want to push your changes to the repo?\n[y]es/[n]o\n")
            if decision == 'n' or decision == 'no':
                return
            elif decision == 'y' or decision == 'yes':
                Git.push(self.data_path)
                break

    def __process_rename_command(self, args):
        print(len(args))
        if len(args) > 3:
            print("Please provide name of the note and new name for it.")
            return
        if len(args) < 3:
            print(
                f"'qn rename takes 2 arguments. {len(args)-1} were provided.")
            return

        note_name = args[1]
        new_note_name = args[2]
        # note doesnt exist
        if self.manifest.contains(note_name) == False:
            print(f"Note {note_name} doesn't exist")
            return
        # new name already occupied
        if self.manifest.contains(new_note_name):
            print(f"Note {new_note_name} already exists")
            return

        old_note_path = path.join(self.data_path, f"{note_name}.md")
        new_note_path = path.join(self.data_path, f"{new_note_name}.md")
        rename(old_note_path, new_note_path)
        self.__update_manifest_file()

    def __process_find_conmmand(self, args):
        if len(args) > 2:
            print(f"'qn find' takes ony argument. {len(args)-1} were provided")
            return

        keyword = args[1]
        notes = [n for n in self.manifest if keyword in n.name]
        if len(notes) == 0:
            print(f"No notes found containing keyword '{keyword}'")
            return

        for n in notes:
            print(n.name)


# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __load_manifest(self):
        content = FileManager.load_file(
            path.join(self.data_path, 'qn.manifest'))
        self.manifest = QnManifest.load(content)

    def __add_to_manifest(self, note_name):
        n = QnManifestElement()
        n.name = note_name
        self.manifest.append(n)
        self.__save_manifest()

    def __save_manifest(self):
        content = QnManifest.dump(self.manifest)
        manifest_path = path.join(self.data_path, 'qn.manifest')
        FileManager.try_create_file(manifest_path, content, True)

    def __update_manifest_file(self):
        files = [f for f in listdir(self.data_path) if f.endswith('.md')]
        self.manifest = QnManifest()
        for f in files:
            self.__add_to_manifest(f.split('.')[0])
        self.__save_manifest()

    def __remove_note_from_manifest(self, note_name):
        notes = [n for n in self.manifest if n.name != note_name]
        self.manifest = QnManifest(notes)
        self.__save_manifest()


class Qnp():
    def process_command(project_name, project_path, args):
        data_path = path.join(project_path, 'notes')
        if data_path[0] == '~':
            data_path = path.expanduser(data_path)
        manifest_path = path.join(data_path, 'qn.manifest')

        Qnp.__init_project_notes(data_path, manifest_path)

        manifest = Qnp.__load_manifest(manifest_path)

        if args[1] == 'new':
            Qnp.__process_new_command(data_path, project_name, manifest, args)
        else:
            print(f"Unkown command {args[1]}")

    def __process_new_command(data_path, project_name, manifest, args):
        note_name = args[2]
        print(len(args))
        if len(args) == 4:
            print("Please provide 'note name'")
            return
        if len(args) > 5:
            print(
                f"'qn new' takes up to 2 arguments. {len(args)-1} were provided."
            )
        if len(args) == 4 and args[3] != '-s':
            print(
                f"Unknown argument {args[3]}. Only known flag argument is '-s'."
            )

        note_name = args[2]
        silent = len(args) == 4
        print(f"note: {note_name}\nsilent: {silent}")

        if FileManager.file_exists(path.join(data_path, note_name)):
            print(f"File {note_name}.md already exists")
            return
        if manifest.contains(note_name):
            print(f"Note already exists in the manifest")
            return

        note_path = path.join(data_path, f"{note_name}.md")
        content = f"# {project_name} - {note_name}"
        FileManager.try_create_file(note_path, content)
        Qnp.__add_to_manifest(manifest, data_path, note_name)

        if silent == False:
            open_vim(note_path)

    def __init_project_notes(data_path, manifest_path):
        if FileManager.directory_exists(data_path) == False:
            FileManager.create_directory(data_path)

        if FileManager.file_exists(manifest_path) == False:
            manifest = QnManifest()
            content = QnManifest.dump(manifest)
            FileManager.try_create_file(manifest_path, content)

# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __load_manifest(manifest_path):
        content = FileManager.load_file(manifest_path)
        return QnManifest.load(content)

    def __add_to_manifest(manifest, data_path, note_name):
        n = QnManifestElement()
        n.name = note_name
        manifest.append(n)
        Qnp.__save_manifest(data_path, manifest)

    def __save_manifest(data_path, manifest):
        print(f"NOTE 0 NAME: {manifest[0].name}")
        content = QnManifest.dump(manifest)
        manifest_path = path.join(data_path, 'qn.manifest')
        FileManager.try_create_file(manifest_path, content, True)


# qn manifest element
class QnManifestElement(Object):
    name = Attribute(type=str)


# qn manifest
class QnManifest(Sequence):
    item_type = QnManifestElement

    def contains(self, note_name):
        notes = [n for n in self if n.name == note_name]
        return len(notes) != 0
