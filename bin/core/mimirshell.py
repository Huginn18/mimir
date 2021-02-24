from cmd import Cmd
from core.helpers import FileManager
from modules.projects import Pm
from yamlize import Attribute, Object


class MimirShell(Cmd):
    def __init__(self):
        # check if ~/.config/ exists
        if FileManager.directory_exists('~/.config/') == False:
            FileManager.create_directory('~/.config')
            print("Created '~/.config/' directory")
        # check if ~/.config/.mimir.d/ exists
        if FileManager.directory_exists('~/.config/.mimir.d/') == False:
            FileManager.create_directory('~/.config/.mimir.d')
            print("Created '~/.config/.mimir.d/' directory")
        # check if ~/.config/.mimirc exists if not create
        if FileManager.file_exists('~/.config/.mimir') == False:
            self.config = Config()
        else:
            config_content = FileManager.load_file('~/.config/.mimir')
            self.config = Config.load(config_content)
        self.__init_modules()

        Cmd.__init__(self)

    def do_quit(self, line):
        """
        exits mimir app
        """
        return True

    do_q = do_quit

    def help_quit(self):
        print(self.do_quit.__doc__)

    def do_pm(self, arg):
        print(arg)


# === == = == === == = == ===
#       Init methods
# === == = == === == = == ===

    def __init_modules(self):
        self.__init_pm_module()

        config_content = Config.dump(self.config)
        FileManager.try_create_file('~/.config/.mimir', config_content)

    def __init_pm_module(self):
        status = self.config.pm_status
        if status == 'default':
            status = 'True'
            self.pm = Pm()
        elif status == 'True':
            self.pm = Pm()
        self.config.pm_status = status


class Config(Object):
    pm_status = Attribute(type=str, default='default')
