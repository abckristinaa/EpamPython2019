import json
import pickle
import pymongo
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
    """ Provides save and read methods with using serialization. """
    @staticmethod
    def save(data, protocol: str, filename: str) -> None:
        """ Saves an object to a library using the given serialization protocol.

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


class MongoDB(Storage):
    def __init__(self, client=None):
        if not client:
            client = input("\nВведите адрес для соединения с БД Mongo."
                           "\nЕсли адрес не введен, будет предпринята попытка "
                           "подключения к БД mongodb.net:27017,library. \n"
                           "Чтобы пропустить, нажмите Enter. \n")
        if client:
            self.client = pymongo.MongoClient(client)
            db_name = input("Введите имя базы данных: \n")
            self.db = self.client[db_name]
        else:
            self.client = pymongo.MongoClient('mongodb://kristy:rfvtym3gg@library-shard-00-00-ags0v.mongodb.net:27017,library-shard-00-01-ags0v.mongodb.net:27017,library-shard-00-02-ags0v.mongodb.net:27017/test?ssl=true&replicaSet=library-shard-0&authSource=admin&retryWrites=true&w=majority')
            self.db = self.client.library

    def save(self, data, protocol, collection_name):
        if protocol.lower() == 'json':
            protocol, key = json, 'json_serial'
        elif protocol.lower() == 'pickle':
            protocol, key = pickle, 'pickle_serial'
        else:
            raise ValueError("Unknown protocol")

        collection = self.db[collection_name]
        collection.drop()
        document_id = collection.insert_one({key: protocol.dumps(data)})
        print(f"Данные успешно сохранены в БД Mongo. \n"
              f"Коллекция: '{collection_name}' \n"
              f"ID документа: {document_id.inserted_id}")

    def read(self, collection_name: str, protocol: str):
        if protocol.lower() == 'json':
            protocol, key = json, 'json_serial'
        elif protocol.lower() == 'pickle':
            protocol, key = pickle, 'pickle_serial'
        else:
            raise ValueError("Unknown protocol")

        collection = self.db[collection_name]
        unserial = list(collection.find())[0][key]
        return protocol.loads(unserial)


if __name__ == "__main__":
    class Foo:
        attr = 'A class attribute'


    my_data = {'key': 'This is an object for JSON and Mongo'}

    FileStorage.save(Foo, "pickle", "new_file")
    file_pickle_from_storage = FileStorage.read("new_file.pickle", "pickle")
    print(file_pickle_from_storage)
    print(file_pickle_from_storage.attr)

    FileStorage.save(my_data, "json", "new_file")
    file_json_from_storage = FileStorage.read("new_file.json", "json")
    print(file_json_from_storage)

    library = MongoDB()
    library.save(my_data, 'pickle', 'test')
    from_mongo_pickle = library.read("test", 'pickle')
    print(from_mongo_pickle)
