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
    def read(self, file: str, protocol: str, arg: str):
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
    """ An interface for saving, reading and deletion documents from Mongo ."""
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://kristy:rfvtym3gg@library-shard-00-00-ags0v.mongodb.net:27017,library-shard-00-01-ags0v.mongodb.net:27017,library-shard-00-02-ags0v.mongodb.net:27017/test?ssl=true&replicaSet=library-shard-0&authSource=admin&retryWrites=true&w=majority')
        self.db = self.client.library

    def save(self, data, protocol, descriprion: str):
        """ Saves an object to a Mongo db with the given serialization protocol.

        A protocol name is used as a collection name. Documents within collection
        is stored as dictionaries {"_id": ID, description: serialized data}

        Args:
            data: A Python object, which will be saved.
            protocol (str): Pickle or json.
            descriprion (str): It is recommended to use a short title that
                               reflects the content of your document.
                               Will be used for searching if ID will not be given.

        Returns:
            docum_id: inserted_id number of saved document.
        """
        if protocol.lower() == 'json':
            protocol, collection_name = json, 'json_serial'
        elif protocol.lower() == 'pickle':
            protocol, collection_name = pickle, 'pickle_serial'
        else:
            raise ValueError("Unknown protocol")

        collection = self.db[collection_name]
        docum_id = collection.insert_one({descriprion: protocol.dumps(data)})
        print(f"Данные успешно сохранены в БД Mongo. \n"
              f"Коллекция: '{collection_name}' \n"
              f"ID документа: {docum_id.inserted_id}\n")
        return docum_id.inserted_id

    def read(self, title: str, protocol: str, doc_id: str = None):
        """ Returns a readable document from Mongo db.

        Documents might be found from database depending on the given args.
        If ID is given method returns exactly this document.
        If descriprion given without ID - method returns all documents with the
        given descriprion.

        Args:
            title (str): A short document title given when saving.
            protocol (str): Pickle or json.
            doc_id (str): Optional, if known.
        Returns:
            unserial: a list of unserialized documents.
        """
        if protocol.lower() == 'json':
            protocol, collection_name = json, 'json_serial'
        elif protocol.lower() == 'pickle':
            protocol, collection_name = pickle, 'pickle_serial'
        else:
            raise ValueError("Unknown protocol")

        collection = self.db[collection_name]
        if not doc_id:
            unserial = list(collection.find({}, {'_id': 0, title: 1}))
            list_docs = [protocol.loads(i[title]) for i in unserial if i]
            return list_docs
        else:
            for i in list(collection.find()):
                if str(i['_id']) == doc_id:
                    key = list(i.keys())[1]
                    return protocol.loads(i[key])

    def delete_collection(self, collection_name: [list, str]):
        """ Clear database from the given collections. """
        if isinstance(collection_name, list):
            for i in collection_name:
                collection = self.db[i]
                collection.drop()
        else:
            collection = self.db[collection_name]
            collection.drop()

        print(f"Коллекции {','.join(collection_name)} успешно удалены.")


if __name__ == "__main__":
    class Foo:
        attr = 'A class attribute'

    my_data = {'key': 'This is an object for JSON and Mongo'}
    mylist = [
        {"name": "Amy", "address": "Apple st 652"},
        {"name": "Hannah", "address": "Mountain 21"},
        {"name": "Michael", "address": "Valley 345"},
        {"name": "Sandy", "address": "Ocean blvd 2"},
        {"name": "Betty", "address": "Green Grass 1"},
        {"name": "Richard", "address": "Sky st 331"},
        {"name": "Susan", "address": "One way 98"},
        {"name": "Vicky", "address": "Yellow Garden 2"},
        {"name": "Ben", "address": "Park Lane 38"},
        {"name": "William", "address": "Central st 954"},
        {"name": "Chuck", "address": "Main Road 989"},
        {"name": "Viola", "address": "Sideway 1633"}
    ]

    FileStorage.save(Foo, "pickle", "new_file")
    file_pickle_from_storage = FileStorage.read("new_file.pickle", "pickle")
    print(file_pickle_from_storage)
    print(file_pickle_from_storage.attr)

    FileStorage.save(my_data, "json", "new_file")
    file_json_from_storage = FileStorage.read("new_file.json", "json")
    print(file_json_from_storage)


    library = MongoDB()
    library.save(my_data, 'pickle', 'first_data')
    library.save(mylist, 'pickle', 'first_data')
    library.save(mylist, 'pickle', 'second_data')

    library.save(my_data, 'json', 'ins_manyyyy')
    library.save(mylist, 'json', 'ins_many')

    library.read('ins_manyyyy', 'json')  # ID is not given
    library.read('ins_manyyyy', 'json', '5e173e1721ffc75aba5faa0a')

    library.delete_collection(['pickle', 'json'])
