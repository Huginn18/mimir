from cmd import Cmd
from core.helpers import FileManager
from yamlize import Attribute, Object


class MimirShell(Cmd):
    def __init__(self):
        # check if ~/.config/ exists
        print(FileManager.directory_exists('~/.config'))
        if FileManager.directory_exists('~/.config/') == False:
            FileManager.create_directory('~/.config')
            print("Created '~/.config/' directory")
        # check if ~/.config/.mimir.d/ exists
        if FileManager.directory_exists('~/.config/.mimir.d/') == False:
            FileManager.create_directory('~/.config/.mimir.d')
            print("Created '~/.config/.mimir.d/' directory")
        # check if ~/.config/.mimirc exists if not create
        if FileManager.file_exists('~/.config/.mimir') == False:
            print('.mimirc not found. Starting init process')
            config = Config()
            config.pm_status = 'foo'
            FileManager.try_create_file('~/.config/.mimir',
                                        Config.dump(config))

        Cmd.__init__(self)

    def do_quit(self, line):
        """
        exits mimir app
        """
        return True

    do_q = do_quit

    def help_quit(self):
        print(self.do_quit.__doc__)


class Config(Object):
    pm_status = Attribute(type=str, default='default')
