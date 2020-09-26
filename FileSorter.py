import os
from shutil import move
from datetime import datetime
import json
import webbrowser as web
from PIL import Image
import base64



def problems_and_features():
    """
    - still cannot run in background
    -
    """


def main():

    def show_how_to_get_sorter_path():
        from b64img import b64_str_img

        image_file_name = "how to get sorter path.jpg"
        if not os.path.exists(image_file_name):
            with open(image_file_name, 'wb') as wf:
                wf.write(base64.b64decode(b64_str_img))
        with Image.open(image_file_name) as image:
            image.show()

    # show read me first
    readme_name = 'FileSorter - README.txt'
    from readme import readme
    if not os.path.exists(readme_name):
        with open(readme_name, 'w') as f:
            f.write(readme)
        web.open(readme_name)

    # check all needed files and read them. If sorter path exists, break.
    while True:
        # create config, if not found
        config = 'FileSorter - config.json'
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
                              f'"D:\Sorter"\n')

        # read config
        move_log = 'FileSorter - move log.txt'
        ignore = [move_log, readme_name]
        ignore_extension = [
            '.!ut', '.adadownload', '.bc', '.bc!', '.blf', '.cache', '.crdownload', '.dmp',
            '.download', '.part', '.partial', '.temp', '.tmp'
        ]
        with open(config, 'r') as f:
            # noinspection PyBroadException
            try:
                data = json.load(f)
                sorter_path = data['sorter path']
                ignore.append(data['ignore'])
                print(f'Sorter path = "{sorter_path}"')
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
        now_str = datetime.now().strftime("%H:%M:%S %d/%m/%y")

        # check for README.txt
        if not os.path.exists(readme_name):
            with open(readme_name, 'w') as f:
                f.write(readme)

        to_put_in_move_log = ""
        for name in in_sorter:
            # noinspection PyBroadException
            try:
                file_name, extension = os.path.splitext(name)
                if not in_sorter:
                    break
                if not os.path.isdir(name) and os.path.isfile(name) \
                        and name not in ignore and extension not in ignore_extension:
                    if not os.path.exists(extension):
                        os.makedirs(extension)

                    old_name_file_path = os.path.join(sorter_path, name)
                    file_name_datetime = datetime.now().strftime('%d%m%y %H%M%S')
                    new_name = f'{file_name} {file_name_datetime}{extension}'
                    new_name_file_path = os.path.join(sorter_path, new_name)
                    os.rename(old_name_file_path, new_name_file_path)
                    dir_name = extension
                    dir_path = os.path.join(sorter_path, dir_name)
                    move(new_name_file_path, dir_path)
                    to_put_in_move_log += f'\nrenamed "{name}" to "{new_name}"\nmoved to {dir_path}\n'
            except:
                pass
            if to_put_in_move_log:
                with open(move_log, 'a', encoding='utf8') as f:
                    f.write(f'{now_str}\n'
                            f'{to_put_in_move_log}'
                            f'{"_" * 100}\n')
    else:
        print('Sorter path does not exist.')
        input('Enter to close ')


if __name__ == '__main__':
    main()
