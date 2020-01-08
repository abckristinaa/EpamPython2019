import json
import pickle
import os
from abc import ABC, abstractmethod


class Storage(ABC):
    """ Defines essential interface for all kind of storages. """
    @abstractmethod
    def save(self, file: str, protocol: str, filename: str):
        pass

    @abstractmethod
    def read(self, file: str, protocol: str):
        pass


class FileStorage:
    """ Provides save and read file methods with using serialization. """
    @staticmethod
    def save(data, protocol: str, filename: str) -> None:
        """ Saves a file to a library using the given serialization protocol.

        Args:
            data: A Python object, which will be saved.
            protocol (str): Pickle or json.
            filename (str): Output filename for saved object.
        """
        filename = filename + '.' + protocol
        if protocol.lower() == 'json':
            flag, protocol = 'w', json
        elif protocol.lower() == 'pickle':
            flag, protocol = 'wb', pickle
        else:
            raise ValueError("Unknown protocol")

        with open(filename, flag) as f:
            protocol.dump(data, f)

        path_to_file = os.getcwd() + '/' + filename
        if os.path.exists(path_to_file):
            print('\nФайл успешно создан: ', path_to_file)
        else:
            print('\nЧто-то пошло не так. Файл не создан.')

    @staticmethod
    def read(file: str, protocol: str):
        """ Returns a file from file storage available to read.

        Args:
            file (str): A name of the file, which will be read.
            protocol (str): Pickle or json.
        """
        if protocol.lower() == 'json':
            flag, protocol = 'r', json
        elif protocol.lower() == 'pickle':
            flag, protocol = 'rb', pickle
        else:
            raise ValueError("Unknown protocol")

        with open(file, flag) as rf:
            data = protocol.load(rf)
        return data





if __name__ == "__main__":
    class Foo:
        attr = 'A class attribute'


    my_data = {'key': 'This is an object for JSON'}

    FileStorage.save(Foo, "pickle", "new_file")
    pickle_from_storage = FileStorage.read("new_file.pickle", "pickle")
    print(pickle_from_storage)
    print(pickle_from_storage.attr)

    FileStorage.save(my_data, "json", "new_file")
    json_from_storage = FileStorage.read("new_file.json", "json")
    print(json_from_storage)
