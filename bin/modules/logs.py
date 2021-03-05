from core.helpers import FileManager, open_vim
from datetime import datetime
from os import path
from yamlize import Object, Attribute, Sequence


class Log():
    def __init__(self, data_path):
        self.data_path = path.join(data_path, 'logs')
        self.__check_folder_structure(data_path)
        self.__load_manifest()

    def process_command(self, arg):
        """
        log help

        new             | opens log file for the day or if it doesn't exist file will be created
        open <date [dd-mm-yyyy]>    | opens log file with specified date
        list <date [mm-yyyy]>       | lists all the logs for the specified month
        """
        args = arg.split()

        if len(args) == 0:
            print('Please provide command for the log module.')
            return

        if args[0] == 'new':
            self.process_new_command()
        else:
            print(f"Unknown command 'log {arg}'.")

    def process_new_command(self, data_path=None):
        now = datetime.now()
        date = now.strftime('%d-%m-%Y')
        time = now.strftime('%H:%M')

        dp = self.data_path
        if data_path != None:
            dp = data_path

        file_name = f"{date}.md"
        file_path = path.join(dp, file_name)

        if FileManager.file_exists(file_path):
            content = f"\n\n# {time}"
            FileManager.append_file(file_path, content)
            open_vim(file_path, True)
        else:
            content = f"# {time}"
            FileManager.try_create_file(file_path, content, False)
            open_vim(file_path, True)

    def process_pm_command(self, project_name, project_path, args):
        """
        logp help

        <project name> new             | opens log file for the day or if it doesn't exist file will be created
        <project name> open <date [dd-mm-yyyy]>    | opens log file with specified date
        <project name> list <date [mm-yyyy]>       | lists all the logs for the specified month
        """
        if len(args) == 1:
            print('Please provide command for the log module.')
            return

        self.__check_folder_structure(path.join(project_path, 'logs'))

        dp = path.expanduser(project_path)
        if args[1] == 'new':
            self.process_new_command(path.join(dp, 'logs'))
        else:
            print(f"Unknown command 'logp {args[0]}'.")

    def __check_folder_structure(self, data_path):
        dp = data_path
        if dp[0] == '~':
            dp = path.expanduser(dp)
        print(f"DP: {dp}")
        manifest_path = path.join(dp, 'log.manifest')

        if FileManager.directory_exists(dp) == False:
            FileManager.create_directory(dp)

        if FileManager.file_exists(manifest_path) == False:
            manifest = LogManifest()
            content = LogManifest.dump(manifest)
            FileManager.try_create_file(manifest_path, content)


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
