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
        elif args[0] == 'list':
            self.__process_list_command(args)
        elif args[0] == 'add':
            self.__process_add_command(args)
        elif args[0] == 'delete':
            self.__process_delete_command(args)
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
        if self.__project_in_manifest(project_name):
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

    def __process_list_command(self, args):
        if len(args) != 1:
            print(
                f"'pm list' doesn't take arguements. {len(args)-1} were provided."
            )
            return

        list = ''
        for p in self.manifest:
            list += f"{p.name} [{p.path}]\n"

        print(list)

    def __process_add_command(self, args):
        if len(args) > 3 or len(args) < 3:
            print(f"`pm add` takes 3 arguments. {len(args)} were provided.")
            return

        project_name = args[1]
        project_path = args[2]
        print(f"project name: {project_name}\npath: {project_path}")

        if FileManager.directory_exists(project_path) == False:
            print(
                f"Directory {project_path} doesn't exist.\n To create project use `pm new` command."
            )
            return
        if self.__project_in_manifest(project_name):
            print(
                f"Project {project_name} already exists. Please provide different name."
            )
            return

        self.__add_project_to_manifest(project_name, project_path)
        # ask for git
        if FileManager.directory_exists(os.path.join(project_path, '.git')):
            print("Git detected in directory")
            return
        else:
            while True:
                decision = helpers.ask(
                    "Do you want to init git in the project?\n[y]es/[n]o")
                if decision == 'y' or decision == 'yes':
                    use_git = True
                    break
                elif decision == 'n' or decision == 'no':
                    return
            Git.create_repo(project_path, project_name)
            Git.first_commit(project_path)

    def __process_delete_command(self, args):
        if len(args) > 2:
            print(
                f"'pm delete' takes only 1 argument. {len(args)-1} were provided."
            )
            return
        if len(args) == 1:
            print(f"Please provide project name")
            return

        project_name = args[1]
        if self.__project_in_manifest(project_name) == False:
            print(f"Unknown project {project_name}")
            return

        project = self.__get_project_from_manifest(project_name)
        delete_dir = False
        while True:
            decision = helpers.ask(
                f"Do you want to delete project directory from your hard drive ({project.path})?\n[y]es/[n]o\n"
            )
            if decision == 'y' or decision == 'yes':
                delete_dir = True
                break
            elif decision == 'n' or decision == 'no':
                break
        if delete_dir:
            FileManager.delete_directory(project.path)

        projects = [p for p in self.manifest if p.name != project_name]
        self.manifest = PmManifest(projects)
        self.__update_manifest_file()
        print(f"Project {project.name} removed.")
        self.__update_manifest_file()


# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __get_project_from_manifest(self, project_name):
        projects = [p for p in self.manifest if p.name == project_name]
        return projects[0]

    def __project_in_manifest(self, project_name):
        projects = [p for p in self.manifest if p.name == project_name]
        return len(projects) == 1

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
