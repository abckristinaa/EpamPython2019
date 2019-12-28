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
    """ Adds get_created_instances, reset_instances_counter methods to a cls:

    Args:
        cls: any class.

    Methods:
        get_created_instances: returns number of created cls instances.
        reset_instances_counter: reset number of cls instances.
      """
    cls.instances = 0
    call_to_cls_init = cls.__init__

    def __init__(self):
        """ Executes cls init, adds instances counter attribute. """
        call_to_cls_init(self)
        cls.instances += 1

    @classmethod
    def get_created_instances(cls):
        """ Returns number of created class instances."""
        return cls.instances

    @classmethod
    def reset_instances_counter(cls):
        """ Resets counter of class instances. """
        result, cls.instances = cls.instances, 0
        return result

    cls.__init__ = __init__
    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter
    return cls


@instances_counter
class User:
    def __init__(self, number=1):
        pass


if __name__ == "__main__":
    print(User.get_created_instances())  # 0
    user, _, _ = User(), User(), User()
    print(user.get_created_instances())  # 3
    print(user.reset_instances_counter())  # 3