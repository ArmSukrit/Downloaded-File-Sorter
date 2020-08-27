import os
from shutil import move
from time import sleep
from datetime import datetime
import json


def problems_and_features():
    """
    - still cannot run in background
    - 
    """


def main():
    check_period = 5
    config = 'config.json'
    readme = f'This folder, "sorter path", is scanned once every {check_period} seconds for new ' \
             f'files and sort them into ' \
             f'their folders based on their extensions\n' \
             f'See move log for move history\n\n' \
             f'IMPORTANT\n' \
             f'\tYou should not create new file in this sorter folder, ' \
             f'because it will be renamed and moved automatically.\n' \
             f'\tIn other word, this folder is suggested to be used as a download folder.\n\n' \
             f'\tAnother useful case, you can use this program to sort other folders by remove "sorter path.txt"\n' \
             f'\tlocated in the same folder as the program. After that rerun the program and it will ask you for ' \
             f'new sorter path".'

    while True:
        # create config, if not found
        if not os.path.exists(config):
            with open(config, 'w') as f:
                pass
            while True:
                path = input("Enter folder path which will be used as sorter\n"
                             "folder path: ")
                print(os.path.exists(path))
                if os.path.exists(path):
                    path_data = {'sorter path': path}
                    with open(config, 'w') as f:
                        json.dump(path_data, f, indent=4, sort_keys=True)
                    break
                else:
                    print(f'cannot find path "{path}"\n'
                          f'For example, if you have a folder named "Sorter" in Drive D:, the path is '
                          f'"D:\Sorter"\n')

        # read config
        with open(config, 'r') as f:
            data = json.load(f)
            sorter_path = data['sorter path']
            print(f'Sorter path = "{sorter_path}"')

        if not os.path.exists(sorter_path):
            print(f'cannot find the folder path specified in {config}')
            os.remove(config)
        else:
            break

    move_log = 'move log.txt'
    readme_name = 'README.txt'
    ignore = [move_log, readme_name]

    if not os.path.exists(readme_name):
        with open(readme_name, 'w') as f:
            f.write(readme)

    os.chdir(sorter_path)
    sorter_path_exists = os.path.exists(sorter_path)
    while sorter_path_exists:
        in_sorter = os.listdir()
        now_str = datetime.now().strftime("%H:%M:%S %d/%m/%y")
        print(f'{now_str} in Sorter: {", ".join(in_sorter)}')

        # check for files, if not found, create.
        for each in ignore:
            if each not in in_sorter:
                with open(each, 'w') as f:
                    if each == readme_name:
                        f.write(readme)

        for name in in_sorter:
            try:
                file_name, extension = name.split('.')
                if not in_sorter:
                    break
                if not os.path.isdir(name) and os.path.isfile(name) and name not in ignore:
                    if not os.path.exists(f'.{extension}'):
                        os.makedirs(f'.{extension}')
                        print(f'folder ".{extension}" has been created.')

                    old_name_file_path = os.path.join(sorter_path, name)
                    file_name_datetime = datetime.now().strftime('%H%M%S %d%m%Y')
                    new_name = f'{file_name} {file_name_datetime}.{extension}'
                    new_name_file_path = os.path.join(sorter_path, new_name)
                    os.rename(old_name_file_path, new_name_file_path)
                    dir_name = f'.{extension}'
                    dir_path = os.path.join(sorter_path, dir_name)
                    move(new_name_file_path, dir_path)
                    with open(move_log, 'a') as f:
                        f.write(f'{now_str} \nrenamed "{name}" to "{new_name}" and moved to {dir_path}\n')

            except:
                pass

        sleep(check_period)
        sorter_path_exists = os.path.exists(sorter_path)

    print('Sorter path does not exist.')
    input('Enter to close ')


if __name__ == '__main__':
    main()
