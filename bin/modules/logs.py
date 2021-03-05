from core.helpers import FileManager
from os import path
from yamlize import Object, Attribute, Sequence


class Log():
    def __init__(self, data_path):
        self.data_path = path.join(data_path, 'logs')
        if self.data_path[0] == '~':
            self.data_path = path.expanduser(self.data_path)
        manifest_path = path.join(self.data_path, 'log.manifest')

        if FileManager.directory_exists(self.data_path) == False:
            FileManager.create_directory(self.data_path)

        if FileManager.file_exists(manifest_path) == False:
            manifest = LogManifest()
            content = LogManifest.dump(manifest)
            FileManager.try_create_file(manifest_path, content)

        self.__load_manifest()

    def process_command(self, arg):
        """
        log help

        new             | opens log file for the day or if it doesn't exist file will be created
        open <date [dd-mm-yyyy]>    | opens log file with specified date
        list <date [mm-yyyy]>       | lists all the logs for the specified month
        """
        pass

    def process_pm_command(self, project_name, project_path, args):
        """
        log help

        <project name> new             | opens log file for the day or if it doesn't exist file will be created
        <project name> open <date [dd-mm-yyyy]>    | opens log file with specified date
        <project name> list <date [mm-yyyy]>       | lists all the logs for the specified month
        """
        pass


# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __load_manifest(self, data_path=None):
        content = FileManager.load_file(
            path.join(self.data_path, 'log.manifest'))
        self.manifest = LogManifest.load(content)


class LogManifestElement(Object):
    name = Attribute(type=str)


class LogManifest(Sequence):
    item_type = LogManifestElement
