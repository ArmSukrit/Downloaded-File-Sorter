import os
from shutil import move
from time import sleep
from datetime import datetime


def problems_and_features():
    """
    - still cannot run in background
    - should create move log to show all moved files
        - should create the log as a txt file with the name of
    """


def main():
    check_period = 5
    save_file_name = 'sorter path.txt'
    readme = f'This folder, "sorter path", is scanned once every {check_period} seconds for new ' \
             f'files and sort them into ' \
             f'their folders based on their extensions\n' \
             f'See move log for move history\n\n' \
             f'IMPORTANT\n' \
             f'\tYou should not create new file in this sorter folder, ' \
             f'because it will be renamed and moved automatically.\n' \
             f'\tIn other word, this folder is suggested to be used as download folder\n\n' \
             f'\tAnother useful case, you can use this program to sort other folders by remove "sorter path.txt"\n' \
             f'\tlocated in the same folder as the program. After that rerun the program and it will ask you for ' \
             f'new sorter path"'

    while True:
        if not os.path.exists(save_file_name):
            with open(save_file_name, 'w') as f:
                while True:
                    path = input("Enter folder path which will be used as sorter\n"
                                 "folder path: ")
                    if os.path.exists(path):
                        f.write(path)
                        break
                    else:
                        print(f'cannot find path "{path}"\n'
                              f'For example, if you have a folder named "Sorter" in Drive D:, the path is '
                              f'"D:\Sorter"\n')

        with open(save_file_name, 'r') as f:
            sorter_path = f.readline()
            print(f'Sorter path = "{sorter_path}"')

        if not os.path.exists(sorter_path):
            print(f'cannot find the folder path specified in {save_file_name}')
            os.remove(save_file_name)
        else:
            break

    os.chdir(sorter_path)
    move_log = 'move log.txt'
    readme_name = 'README.txt'
    ignore = [move_log, readme_name]

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
