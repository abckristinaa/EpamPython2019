import json
import pickle
import os
from abc import ABC, abstractmethod


class Storage(ABC):
    """ Defines essential interface for all kind of storages. """
    @abstractmethod
    def save_to_library(self, file: str, protocol: str, filename: str):
        pass

    @abstractmethod
    def read_from_library(self, file: str, protocol: str, filename: str):
        pass


class FileStorage:
    """ Provides save and read file methods with using serialization. """
    @staticmethod
    def save(file: str, protocol: str, filename: str) -> None:
        """ Saves a file to library using the given serialization protocol.

        Args:
            file (str): A name of the file, which will be saved.
            protocol (str): Pickle or json.
            filename (str): Output filename.
        """
        if protocol.lower() == 'json':
            flag, protocol = 'w', json
        elif protocol.lower() == 'pickle':
            flag, protocol = 'wb', pickle
        else:
            raise ValueError("Unknown protocol")

        with open(filename, flag) as f:
            protocol.dump(file, f)

        path_to_file = os.getcwd() + '/' + filename
        if os.path.exists(path_to_file):
            print('\nФайл успешно создан: ', path_to_file)
        else:
            print('\nЧто-то пошло не так. Файл не создан.')

    @staticmethod
    def read(file: str, protocol: str, filename: str):
        """ Returns a file from file storage available to read.

        Args:
            file (str): A name of the file, which will be read.
            protocol (str): Pickle or json.
            filename (str): Output filename.
        """
        if protocol.lower() == 'json':
            flag, protocol = 'r', json
        elif protocol.lower() == 'pickle':
            flag, protocol = 'rb', pickle
        else:
            raise ValueError("Unknown protocol")

        with open(file, flag) as rf:
            with open(filename, "w") as wf:
                data = protocol.load(rf)
                wf.write(data)


if __name__ == "__main__":
    FileStorage.save("hw.txt", "pickle", "new_file")
    FileStorage.read("new_file", "pickle", "new_file.txt")
