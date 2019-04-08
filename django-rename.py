#!/usr/bin/python3

import argparse
import errno
import os
import sys
from fileinput import FileInput

def update_project_files(path, old_name, new_name):
    """
    Updates Django project files by replacing old project name
    with the new project name.

    :param path: The project folder
    :param old_name: The old project name
    :param new_name: The new project name
    """
    manage_path = os.path.join(path, "manage.py")
    if not os.path.exists(manage_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), manage_path)

    settings_path = os.path.join(path, old_name, "settings.py")
    if not os.path.exists(settings_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), settings_path)

    wsgi_path = os.path.join(path, old_name, "wsgi.py")
    if not os.path.exists(wsgi_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), wsgi_path)

    files = [manage_path, settings_path, wsgi_path]
    for filename in files:
        with FileInput(filename, inplace=True, backup=".bak") as f:
            for line in f:
                sys.stdout.write(line.replace(old_name, new_name))

def get_project_name(path):
    """
    Returns the name of the Django project in given path.

    :param path: The projects folder
    :rtype: String name of the project
    """
    return os.path.basename(os.path.abspath(path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("project_folder", type=str)
    parser.add_argument("name", type=str)
    args = parser.parse_args()

    project_name = get_project_name(args.project_folder)
    update_project_files(args.project_folder, project_name, args.name)

    absolute_path = os.path.abspath(args.project_folder)
    dirname = os.path.dirname(absolute_path)
    settings_dir = os.path.join(absolute_path, project_name)
    os.rename(settings_dir, os.path.join(absolute_path, args.name))
    os.rename(absolute_path, os.path.join(dirname, args.name))



