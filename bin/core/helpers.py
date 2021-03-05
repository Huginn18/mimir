from git import Repo
import os
from os import path, environ, remove
from subprocess import call
import subprocess


def ask(question):
    anwser = ''
    while True:
        anwser = input(question)
        if anwser != '':
            return anwser


def open_vim(path, end_of_file=False):
    editor = environ.get('EDITOR', 'vim')
    if end_of_file:
        call([editor, '+', path])
    else:
        call([editor, path])


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

    def delete_directory(_path):
        full_path = _path
        if full_path[0] == '~':
            full_path = FileManager.__expand_path(full_path)

        try:
            import shutil
            shutil.rmtree(full_path, ignore_errors=True)
            print(f"Delted directory {full_path}")
        except OSError as e:
            print("Error: %s : %s" % (full_path, e.strerror))

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

    def delete_file(_path):
        full_path = _path
        if full_path[0] == '`':
            full_path = path.expanduser(full_path)
        remove(full_path)

    def append_file(_path, content):
        full_path = _path
        if full_path[0] == '~':
            full_path = path.expanduser(full_path)

        with open(full_path, 'a') as file:
            return file.write(content)

    def __expand_path(_path):
        return path.expanduser(_path)


class Git():
    def create_repo(_path, project_name):
        privacy = ''
        while True:
            decision = ask(
                "Visibility:\n[1] public\n[2] private\n[3] internal\n")
            if decision == '1':
                privacy = '--public'
                break
            elif decision == '2':
                privacy = '--private'
                break
            elif decision == '3':
                privacy = '--internal'
                break
        os.chdir(os.path.expanduser(os.path.dirname(_path)))

        p = subprocess.Popen(
            ['gh', 'repo', 'create', project_name, '--confirm', privacy])
        out, err = p.communicate()
        print(out)

    def first_commit(_path):
        readme_path = path.expanduser(path.join(_path, 'readme.md'))
        with open(readme_path, 'w') as file:
            file.write(f"# {readme_path.split('/')[-1]}")

        os.chdir(path.expanduser(_path))
        p = subprocess.Popen(['git', 'add', '.'])
        out, err = p.communicate()
        p = subprocess.Popen(['git', 'commit', '-m', "'initial commit'"])
        out, err = p.communicate()
        p = subprocess.Popen(
            ['git', 'push', '--set-upstream', 'origin', 'main'])
        p.wait()

    def status(_path):
        os.chdir(path.expanduser(_path))
        try:
            output = subprocess.check_output(['git', 'status'])
            return output
        except subprocess.CalledProcessError as e:
            return 'fatal'

    def add_all(_path):
        os.chdir(path.expanduser(_path))
        subprocess.check_output(['git', 'add', '.'])

    def commit(_path):
        os.chdir(path.expanduser(_path))
        subprocess.call('git commit', shell=True)

    def push(_path):
        os.chdir(path.expanduser(_path))
        subprocess.check_output(['git', 'push'])
