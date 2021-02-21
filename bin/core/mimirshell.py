from cmd import Cmd


class MimirShell(Cmd):
    def do_quit(self, line):
        """
        exits mimir app
        """
        return True

    do_q = do_quit

    def help_quit(self):
        print(self.do_quit.__doc__)
