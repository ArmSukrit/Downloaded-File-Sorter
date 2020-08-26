import os
from shutil import move
from time import sleep
from datetime import datetime


def known_problems():
    """
    - still cannot run in background
    """


def main():
    check_period = 30
    save_file_name = 'sorter path.txt'
    readme = f'This program checks sorter path every {check_period} seconds for new files and sort them into ' \
             f'their folders based on their extension'

    if not os.path.exists('README.txt'):
        with open('README.txt', 'w') as f:
            f.write(readme)

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

    sorter_path_exists = os.path.exists(sorter_path)
    while sorter_path_exists:
        os.chdir(sorter_path)
        in_sorter = os.listdir()
        now_str = datetime.now().strftime("%H:%M:%S %d/%m/%y")
        print(f'{now_str} in Sorter: {", ".join(in_sorter)}')
        for name in in_sorter:
            try:
                file_name, extension = name.split('.')
                if not in_sorter:
                    break
                if not os.path.isdir(name) and os.path.isfile(name):
                    if not os.path.exists(f'.{extension}'):
                        os.makedirs(f'.{extension}')
                        print(f'folder ".{extension}" has been created.')

                    old_name_file_path = os.path.join(sorter_path, name)
                    file_name_datetime = datetime.now().strftime('%H%M%S %d%m%Y')
                    new_name = f'{file_name} {file_name_datetime}.{extension}'
                    new_name_file_path = os.path.join(sorter_path, new_name)
                    os.rename(old_name_file_path, new_name_file_path)
                    dir_name = f'.{extension}'
                    move(new_name_file_path, os.path.join(sorter_path, dir_name))
                    print(f'moved {old_name_file_path} to {new_name_file_path}')
            except:
                pass

        sleep(check_period)
        sorter_path_exists = os.path.exists(sorter_path)

    print('Sorter path does not exist.')
    input('Enter to close')


if __name__ == '__main__':
    main()
