from core import helpers
from core.helpers import FileManager
from core.helpers import Git
import os
import subprocess
from yamlize import Sequence, Object, Attribute


class Pm():
    def __init__(self):
        if FileManager.file_exists('~/.config/.mimir.d/pm.manifest') == False:
            manifest = PmManifest()

            element = PmElement()
            element.name = "foo"
            element.path = "~/projects/foo"
            manifest.append(element)

            content = PmManifest.dump(manifest)
            FileManager.try_create_file('~/.config/.mimir.d/pm.manifest',
                                        content)
        self.__load_manifest()

    def process_command(self, arg):
        """
        pm  help

        Module for registering and managing projects.

        Commands list:
            new <project name> <path>   | adds project 'project name' to the registry and creates directory for it
            add <project name> <path>   | adds already existing project to registry as 'project name' at 'path'
            list                        | lists all projects in registry
            delete <project name>       | deletes 'project name' from registry
        """
        args = arg.split()
        if len(args) == 0:
            print("Please provide command. If you need help use 'help pm'")
            return
        if args[0] == 'new':
            self.__process_new_command(args)
        else:
            print(f"Unknown command 'pm {args[0]}'.")

    def __process_new_command(self, args):
        if len(args) > 3 or len(args) < 3:
            print(f"'pm new' takes 2 arguments. {len(args)-1} were provided.")
            return

        project_name = args[1]
        path = args[2]
        print(f"project name: {project_name}\npath: {path}")
        # check if directory or project exists
        projects = [p for p in self.manifest if p.name == project_name]
        if len(projects) != 0:
            print(
                f"Project {project_name} already exists. Please provide different name."
            )
            return

        if FileManager.directory_exists(path):
            print(f"Directory {path} already exists.")
            return
        else:
            # create dir
            FileManager.create_directory(path)
            print(f"{path} created")
            # ask user if they want to use git
            use_git = False
            while True:
                decision = helpers.ask(
                    'Do you want to set up gh project?\n[y]es/[n]o\n')
                if decision == 'y' or decision == 'yes':
                    use_git = True
                    break
                elif decision == 'n' or decision == 'no':
                    return
            Git.create_repo(path, project_name)
            Git.first_commit(path)
            self.__add_project_to_manifest(project_name, path)


# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __add_project_to_manifest(self, project_name, path):
        p = PmElement()
        p.name = project_name
        p.path = path
        self.manifest.append(p)
        self.__update_manifest_file()

    def __load_manifest(self):
        content = FileManager.load_file('~/.config/.mimir.d/pm.manifest')
        self.manifest = PmManifest.load(content)

    def __update_manifest_file(self):
        content = PmManifest.dump(self.manifest)
        FileManager.try_create_file('~/.config/.mimir.d/pm.manifest', content,
                                    True)


class PmElement(Object):
    name = Attribute(type=str)
    path = Attribute(type=str)


class PmManifest(Sequence):
    item_type = PmElement
