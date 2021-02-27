from core.helpers import FileManager
from yamlize import Sequence, Object, Attribute


# qn class
class Qn():
    def __init__(self):
        if FileManager.file_exists('~/.config/.mimir.d/qn.manifest') == False:
            manifest = QnManifest()
            content = QnManifest.dump(manifest)
            FileManager.try_create_file('~/.config/.mimir.d/qn.manifest',
                                        content)
        self.__load_manifest()

# === == = == === == = == ===
#       REGION: Manifest
# === == = == === == = == ===

    def __load_manifest(self):
        content = FileManager.load_file('~/.config/.mimir.d/qn.manifest')
        self.manifest = QnManifest.load(content)


# qn manifest element
class QnManifestElement(Object):
    name = Attribute(type=str)


# qn manifest
class QnManifest(Sequence):
    item_type = QnManifestElement
