"""
Реализовать метод __str__, позволяющий выводить все папки и файлы из данной,
например так:
> print(folder1)
V folder1
|-> V folder2
|   |-> V folder3
|   |   |-> file3
|   |-> file2
|-> file1
А так же возможность проверить, находится ли файл или папка в другой папке:
> print(file3 in folder2)
True
"""

import os


class PrintableFolder:
    def __init__(self, name: str):
        self.path = name

    def getcontext(self) -> list:
        context = []
        path_len = len(self.path.split('/'))
        for root, _, files in os.walk(self.path):
            root_ = root.split('/')
            root_len = len(root_)
            idx = '|   ' * (root_len - path_len)
            context.append(f'{idx}|-> V {root_[-1]}')
            for file in files:
                context.append(f'{idx}|-> {file}')
        return context

    def __str__(self):
        return "\n".join(self.getcontext() + [""])

    def __contains__(self, item: str):
        for _, dirs, file in os.walk(self.path):
            if item in file or item in dirs:
                return True
        else:
            return False


if __name__ == "__main__":
    folder1 = PrintableFolder('/home/abckristinaa/PycharmProjects/epam/EpamPython2019/01-Data-Structures')
    folder2 = PrintableFolder('/home/abckristinaa/PycharmProjects/epam/EpamPython2019/13-design-patterns')

    print(folder1)
    print(folder2)

    file2 = 'design_patterns_lections.pdf'
    file3 = 'homework_strings.py'
    file5 = 'docum'
    folder6 = '2-adapter'
    folder7 = 'adapter'

    print(file3 in folder1)     #True
    print(file5 in folder2)     #False
    print(file2 in folder2)     #True
    print(file2 in folder1)     #False

    print(folder6 in folder2)     # True
    print(folder7 in folder2)       # False