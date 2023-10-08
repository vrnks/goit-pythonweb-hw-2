from pathlib import Path
import shutil
import file_parser as parser
import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r",
               "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    normalized_name = name.translate(TRANS)
    normalized_name = re.sub(r'\W^.', '_', normalized_name)
    return normalized_name


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        try:
            shutil.unpack_archive(filename, folder_for_file)
        except shutil.ReadError:
            folder_for_file.rmdir()
    except OSError:
        print(f"{OSError}: ваші архіви видалено!")
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")


def main():
    while True:
        input_line = input(
            'Please select your folder to sort. For exit, type "exit": ')
        if input_line == "exit":
            break
        folder = Path(input_line)
        parser.scan(folder)
        for file in parser.JPEG_IMAGES:
            handle_media(file, folder / 'images' / 'JPEG')
        for file in parser.JPG_IMAGES:
            handle_media(file, folder / 'images' / 'JPG')
        for file in parser.PNG_IMAGES:
            handle_media(file, folder / 'images' / 'PNG')
        for file in parser.SVG_IMAGES:
            handle_media(file, folder / 'images' / 'SVG')
        for file in parser.MP3_AUDIO:
            handle_media(file, folder / 'audio')
        for file in parser.MP4_VIDEO:
            handle_media(file, folder / 'video')

        for file in parser.MY_OTHER:
            handle_media(file, folder / 'MY_OTHER')
        for file in parser.ARCHIVES:
            handle_archive(file, folder / 'ARCHIVES')

        for folder in parser.FOLDERS[::-1]:
            handle_folder(folder)
        print('The folder has been succesfully sorted')


if __name__ == "__main__":
    main()
