import base64
import json
import os
import sys
import webbrowser as web
from datetime import datetime
from os.path import join
from shutil import Error, move

from b64img import b64_str_img
from readme import readme

try:
    from PIL import Image
except ImportError:
    os.system(sys.executable + " -m pip install -r requirements.txt")
    input("Restart to continue...")
    exit(0)


# global variables
script_path = os.path.abspath(__file__)
readme += f'- This program is at {script_path}'
script_dir = os.path.dirname(script_path)
CONFIG = 'FileSorter - config.json'
readme_name = 'FileSorter - README.txt'
move_log = 'FileSorter - move log.csv'
IGNORED_FILES = [move_log, readme_name]
image_file_name = "how to get sorter path.jpg"


def show_how_to_get_sorter_path():
    if not os.path.exists(image_file_name):
        with open(image_file_name, 'wb') as wf:
            wf.write(base64.b64decode(b64_str_img))
    with Image.open(image_file_name) as image:
        image.show()


def show_readme():
    # show read me first
    try:
        f = open(readme_name)
    except FileNotFoundError:
        with open(readme_name, 'w') as f:
            f.write(readme)
        web.open(readme_name)
    else:
        f.close()


def main():
    # change cwd to the directory of this script
    os.chdir(script_dir)

    # check all needed files in script_dir and read them.
    show_readme()  # if doesn't exist
    create_config()  # if doesn't exist
    ignored_extensions = get_ignored_extensions()
    paths: list = get_paths()

    for path in paths:
        if not os.path.isdir(path):
            print(f'{path} doesn\'s exist')
            continue
        sort_files(path, ignored_extensions)


def get_paths():
    # read config to get paths
    with open(CONFIG, 'r') as f:
        # noinspection PyBroadException
        try:
            data = json.load(f)
            paths = data['sorter paths']
            for file in data["ignore"]:
                IGNORED_FILES.append(file)
            print(f'Sorter path = {paths}\n')
        except:
            print('Invalid config, recreating it...')
            f.close()
            os.remove(CONFIG)
    return paths


def get_ignored_extensions():
    # get temp file extensions
    with open('common temporary file extensions.json') as f:
        data = json.load(f)
        ignored_extensions = [each["extension"]
                              for each in data["common extensions"]]
    return ignored_extensions


def create_config():
    # create config, if not found
    if not os.path.exists(CONFIG):
        all_config = {
            'sorter paths': [], 'ignore': ['example.txt']
        }
        show_how_to_get_sorter_path()
        with open(CONFIG, 'w') as f:
            # get sorter path
            print("Enter x to stop adding path.")
            while True:
                path = input("Enter folder path which will be used as sorter\n"
                             "sorter path = ").strip().strip('"')
                if path == "x":
                    break
                if os.path.exists(path):
                    all_config['sorter paths'].append(path)
                else:
                    print(f'cannot find path "{path}"\n'
                          f'For example, if you have a folder named "Sorter" in D:, the path is '
                          f'"D:\\Sorter"\n')
            json.dump(all_config, f, indent=4)


def sort_files(path: str, ignored_extensions: list):
    """ sort files based on their extensions in sorter_path directory """

    os.chdir(path)  # from now on, work in path

    # check for README.txt
    if not os.path.exists(readme_name):
        with open(readme_name, 'w') as f:
            f.write(readme)

    # check for move log
    if not os.path.exists(move_log):
        with open(move_log, "w") as f:
            f.write("old,current,moved_to,move_date,move_time\n")

    all_files = os.listdir()
    cared_files = [file for file in all_files if file not in IGNORED_FILES]
    if not cared_files:
        return
    to_put_in_move_log = []
    to_report = {}
    for name in cared_files:
        try:
            file_name, extension = os.path.splitext(name)
            if not os.path.isdir(name) and os.path.isfile(name) and extension not in ignored_extensions:
                if not os.path.exists(extension):
                    os.makedirs(extension)

                old_name_file_path = os.path.join(path, name)
                now = datetime.now()
                os.chdir(os.path.join(path, extension))
                if os.path.exists(name):
                    file_name_datetime = now.strftime('time-%H%M%S')
                    new_name = f'{file_name} {file_name_datetime}{extension}'
                else:
                    new_name = file_name + extension
                os.chdir(path)
                new_name_file_path = os.path.join(path, new_name)
                os.rename(old_name_file_path, new_name_file_path)
                dir_name = extension
                dir_path = os.path.join(path, dir_name)
                move(new_name_file_path, dir_path)
                to_report[name] = dir_path
                items = [name, new_name, dir_path + '\\', now.strftime(
                    "%d/%m/%Y"), now.strftime("%H:%M:%S")]
                to_put_in_move_log.append(items)
        except Error as e:
            print(e)
    if to_put_in_move_log:
        with open(move_log, 'a', encoding='utf8') as f:
            for each in to_put_in_move_log:
                f.write(",".join(each) + '\n')
    if to_report:
        print('moved')
        for name, new_path in to_report.items():
            print(f'- {name} to {new_path}\\')
        input()


if __name__ == '__main__':
    main()
