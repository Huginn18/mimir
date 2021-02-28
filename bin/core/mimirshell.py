from cmd import Cmd
from core.helpers import FileManager, ask
from modules.projects import Pm
from modules.quicknote import Qn
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
        self.pm.process_command(arg)

    def help_pm(self):
        print(self.pm.process_command.__doc__)


# === == = == === == = == ===
#       Init methods
# === == = == === == = == ===

    def __init_modules(self):
        self.__init_pm_module()
        self.__init_qn_module()

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

    def __init_qn_module(self):
        status = self.config.qn_status

        if status == 'default':
            use = False
            while True:
                decision = ask(
                    'Do you want to initialise quick note module?\n[y]es/[n]o\n'
                )
                if decision == 'y' or decision == 'yes':
                    use = True
                    break
                elif decision == 'n' or decision == 'no':
                    break
            if use:
                status = 'True'
                self.qn = Qn()
        elif status == 'True':
            self.qn = Qn()
        else:
            self.qn = None

        self.config.qn_status = status


class Config(Object):
    pm_status = Attribute(type=str, default='default')
    qn_status = Attribute(type=str, default='default')
