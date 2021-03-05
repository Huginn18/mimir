from cmd import Cmd
from core.helpers import FileManager, ask
from modules.projects import Pm
from modules.quicknote import Qn, Qnp
from yamlize import Attribute, Object


class MimirShell(Cmd):
    def __init__(self):
        if FileManager.directory_exists('~/.config/') == False:
            FileManager.create_directory('~/.config')
            print("Created '~/.config/' directory")
        if FileManager.directory_exists('~/.config/.mimir.d/') == False:
            FileManager.create_directory('~/.config/.mimir.d')
            print("Created '~/.config/.mimir.d/' directory")
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

    def do_qn(self, arg):
        if self.qn == None:
            print("'qn' module is not initialized.")
            return
        self.qn.process_command(arg)

    def do_qnp(self, arg):
        args = arg.split()
        project = self.pm.get_project_from_manifest(args[0])
        Qnp.process_command(project.name, project.path, args)

    def help_qnp(self):
        print(Qnp.process_command.__doc__)

    def help_qn(self):
        print(self.qn.process_command.__doc__)


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
                self.__init_qn_moudle_data_path()
                self.qn = Qn(self.config.qn_data_path)
        elif status == 'True':
            self.qn = Qn(self.config.qn_data_path)
        else:
            self.qn = None

        self.config.qn_status = status

    def __init_qn_moudle_data_path(self):
        path = '~/.mimir'
        use_custom_path = False
        while True:
            decision = ask(
                'Do you want to set custom loction for notes directory?\nDefault: ~/.mimir\n[y]es/[n]o'
            )
            if decision == 'y' or decision == 'yes':
                use_custom_path = True
                break
            elif decision == 'n' or decision == 'no':
                break
        if use_custom_path:
            path = ask('Please provide new path\n')

        self.config.qn_data_path = path


class Config(Object):
    pm_status = Attribute(type=str, default='default')
    qn_status = Attribute(type=str, default='default')
    qn_data_path = Attribute(type=str, default='~/.mimir')
