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
readme_name = 'FileSorter - README.txt'
config = 'FileSorter - config.json'
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

    show_readme()

    # check all needed files and read them. If sorter path exists, break.
    while True:
        # create config, if not found
        if not os.path.exists(config):
            all_config = {
                'sorter path': None, 'ignore': ['example.txt']
            }
            show_how_to_get_sorter_path()
            with open(config, 'w') as f:
                # get sorter path
                while True:
                    path = input("Enter folder path which will be used as sorter\n"
                                 "sorter path = ").strip().strip('"')
                    if os.path.exists(path):
                        all_config['sorter path'] = path
                        json.dump(all_config, f, indent=4)
                        break
                    else:
                        print(f'cannot find path "{path}"\n'
                              f'For example, if you have a folder named "Sorter" in Drive D:, the path is '
                              f'"D:\\Sorter"\n')

        # get temp file extensions
        with open('common temporary file extensions.json') as f:
            data = json.load(f)
            ignore_extension = [each["extension"]
                                for each in data["common extensions"]]

        # read config
        move_log = 'FileSorter - move log.csv'
        ignore = [move_log, readme_name]
        with open(config, 'r') as f:
            # noinspection PyBroadException
            try:
                data = json.load(f)
                sorter_path = data['sorter path']
                ignore.append(data['ignore'])
                print(f'Sorter path = "{sorter_path}"\n')
                if not os.path.exists(sorter_path):
                    print(f'cannot find the folder path specified in {config}')
                    show_how_to_get_sorter_path()
                    os.remove(config)
                else:
                    break
            except:
                print('Invalid config, recreating it...')
                f.close()
                os.remove(config)

    # main program
    os.chdir(sorter_path)
    sorter_path_exists = os.path.exists(sorter_path)
    if sorter_path_exists:
        in_sorter = os.listdir()
        in_sorter = [name for name in in_sorter if name not in ignore]

        # check for README.txt
        if not os.path.exists(readme_name):
            with open(readme_name, 'w') as f:
                f.write(readme)

        # check for move log
        if not os.path.exists(move_log):
            with open(move_log, "w") as f:
                f.write("old,current,moved_to,move_date,move_time\n")

        to_put_in_move_log = []
        to_report = {}
        for name in in_sorter:
            try:
                file_name, extension = os.path.splitext(name)
                if not in_sorter:
                    break
                if not os.path.isdir(name) and os.path.isfile(name) \
                        and name not in ignore and extension not in ignore_extension:
                    if not os.path.exists(extension):
                        os.makedirs(extension)

                    old_name_file_path = os.path.join(sorter_path, name)
                    now = datetime.now()
                    os.chdir(os.path.join(sorter_path, extension))
                    if os.path.exists(name):
                        file_name_datetime = now.strftime('time-%H%M%S')
                        new_name = f'{file_name} {file_name_datetime}{extension}'
                    else:
                        new_name = file_name + extension
                    os.chdir(sorter_path)
                    new_name_file_path = os.path.join(sorter_path, new_name)
                    os.rename(old_name_file_path, new_name_file_path)
                    dir_name = extension
                    dir_path = os.path.join(sorter_path, dir_name)
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
    else:
        print('Sorter path does not exist.')
        input('Enter to close ')


if __name__ == '__main__':
    main()
