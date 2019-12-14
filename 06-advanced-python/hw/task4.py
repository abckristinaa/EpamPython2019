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
    def __init__(self, name):
        self.name = name

    def getpath(self):
        for root, dirs, file in os.walk('/home/'):
            if self.name in dirs:
                return os.path.join(root, self.name)

    def getcontext(self):
        context = []
        path = self.getpath()
        path_len = len(path.split('/'))
        for root, dirs, files in os.walk(path):
            root_ = root.split('/')
            root_len = len(root_)
            idx = '|   ' * (root_len - path_len)
            context.append(f'{idx}|-> V {root_[-1]}')
            for file in files:
                context.append(f'{idx}|-> {file}')
        return context

    def __str__(self):
        return "\n".join(self.getcontext() + [""])

    def __contains__(self, item):
        for root, dirs, file in os.walk(self.getpath()):
            if item in file or item in dirs:
                return True
            else:
                False


if __name__ == "__main__":
    folder1 = PrintableFolder('01-Data-Structures')
    folder2 = PrintableFolder('11-Design_Patterns')

    print(folder1)
    print(folder2)

    file2 = '2.xml'
    file3 = 'homework_strings.py'
    file5 = 'documents'

    print(file3 in folder1)
    print(file5 in folder2)
    print(file2 in folder2)
    print(file2 in folder1)
