"""
Задание 2
Написать маленькую утилиту, которая в качестве аргумента принимает путь до директории и sha256 hash

Утилита должна пройти по всем файлам внутри директории и вывести в stdout абсолютный путь до файлов,
хеш которых указан в качестве аргумента

Определить:
1) какой системный вызов будет использоваться чаще всего (strace)
2) какой участок кода "самый горячий" (профилирование)
3) какой системный вызов потребил больше всего времени (strace + анализ логов)
"""

import argparse
import hashlib
import os


BUF_SIZE = 102400


def get_sha256_hash(root: str, file: str) -> str:
    """ Generates sha256 hash for given file. Returns it in hexdigest. """
    with open(os.path.join(root, file), 'rb') as f:
        sha = hashlib.sha256()
        while True:
            data = f.read()
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def main() -> str:
    """ Returns abs path to file in directory by given sha256 hash. """
    parser = argparse.ArgumentParser(description='Finds files by their '
                                                 'sha256 hash.')
    parser.add_argument('path_to_dir', type=str, help='Input dir path')
    parser.add_argument('file_hash', type=str, help='Input sha256 hash')
    args = parser.parse_args()

    if args.path_to_dir.endswith('/'):
        args.path_to_dir = args.path_to_dir[:-1]

    for root, dirs, files in os.walk(args.path_to_dir):
        for file in files:
            if get_sha256_hash(root, file) == args.file_hash:
                return f"Path to file: {root}/{file}"
    else:
        return "File not found."


if __name__ == "__main__":
    print(main())
