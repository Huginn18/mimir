import os
from os import path


class FileManager():
    def file_exists(_path):
        if _path[0] == '~':
            return path.isfile(FileManager.__expand_path(_path))

        return path.isfile(_path)

    def directory_exists(_path):
        if _path[0] == '~':
            return path.isdir(FileManager.__expand_path(_path))

        return path.isdir(_path)

    def create_directory(_path):
        full_path = _path
        if full_path[0] == '~':
            full_path = FileManager.__expand_path(full_path)

        os.mkdir(full_path)

    def try_create_file(path, content='', override=False):
        full_path = FileManager.__expand_path(path)
        if FileManager.file_exists(full_path):
            if override:
                with open(full_path, 'w') as file:
                    file.write(content)
                return True
            else:
                return False
        with open(full_path, 'w') as file:
            file.write(content)
        return True

    def load_file(_path):
        full_path = _path
        if full_path[0] == '~':
            full_path = path.expanduser(full_path)

        with open(full_path, 'r') as file:
            return file.read()

    def __expand_path(_path):
        return path.expanduser(_path)
