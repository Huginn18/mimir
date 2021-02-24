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
        args = arg.split()
        print(args)


class PmElement(Object):
    name = Attribute(type=str)
    path = Attribute(type=str)


class PmManifest(Sequence):
    item_type = PmElement
