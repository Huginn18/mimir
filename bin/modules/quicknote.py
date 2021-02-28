from core.helpers import FileManager
from os import path, environ
from subprocess import call
from yamlize import Sequence, Object, Attribute


# qn class
class Qn():
    def __init__(self, data_path):
        self.data_path = path.join(data_path, 'notes')
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
        """
        args = arg.split()
        if len(args) == 0:
            print("Please provide command. If you need help use 'help qn'")
            return
        if args[0] == 'new':
            self.__process_new_command(args)
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
        if note_path[0] == '~':
            note_path = path.expanduser(note_path)

        content = f"# {note_name}"
        FileManager.try_create_file(note_path, content)
        self.__add_to_manifest(note_name)
        self.__save_manifest()
        EDITOR = environ.get('EDITOR', 'vim')
        call([EDITOR, note_path])

# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __load_manifest(self):
        content = FileManager.load_file('~/.config/.mimir.d/qn.manifest')
        self.manifest = QnManifest.load(content)

    def __add_to_manifest(self, note_name):
        n = QnManifestElement()
        n.name = note_name
        self.manifest.append(n)

    def __save_manifest(self):
        content = QnManifest.dump(self.manifest)
        manifest_path = path.join(self.data_path, 'qn.manifest')
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
