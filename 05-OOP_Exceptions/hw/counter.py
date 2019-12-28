"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    """ Returns wrapper class. """

    class wrapper:
        """Adds two methods to the given class. """
        def __init__(self, *args, **kwargs):
            cls(*args, **kwargs)
            cls.instances += 1

        @staticmethod
        def get_created_instances():
            """ Returns number of created class instances."""
            return cls.instances

        @staticmethod
        def reset_instances_counter():
            """ Resets counter of class instances. """
            result, cls.instances = cls.instances, 0
            return result

    cls.instances = 0
    return wrapper


@instances_counter
class User:
    def __init__(self, number=1):
        pass


if __name__ == "__main__":
    print(User.get_created_instances())  # 0
    user, _, _ = User(), User(), User()
    print(user.get_created_instances())  # 3
    print(user.reset_instances_counter())  # 3
    print(User.get_created_instances())  # 0
