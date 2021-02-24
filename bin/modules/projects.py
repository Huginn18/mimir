from core.helpers import FileManager
from yamlize import Sequence, Object, Attribute


class Pm():
    def __init__(self):
        if FileManager.file_exists('~/.config/.mimir.d/pm.manifest') == False:
            manifest = PmManifest()
            content = PmManifest.dump(manifest)
            FileManager.try_create_file('~/.config/.mimir.d/pm.manifest',
                                        content)
        self.__load_manifest()

    def __load_manifest(self):
        content = FileManager.load_file('~/.config/.mimir.d/pm.manifest')
        self.manifest = PmManifest.load(content)

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
        print(args)
        if len(args) == 0:
            print("Please provide command. If you need help use 'help pm'")


class PmElement(Object):
    name = Attribute(type=str)
    path = Attribute(type=str)


class PmManifest(Sequence):
    item_type = PmElement
