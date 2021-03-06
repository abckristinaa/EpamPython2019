"""

Реализовать такой метакласс, что экземпляры класса созданного с помощью него
будут удовлетворять следующим требованиям:

* объекты созданные с одинаковыми аттрибутами будут одним и тем же объектом
* объекты созданные с разными аттрибутами будут разными объектами
* у любого объекта есть мозможность получить доступ к другим объектам
    того же класса


>>> unit1 = SiamObj('1', '2', a=1)
>>> unit2 = SiamObj('1', '2', a=1)
>>> unit1 is unit2
True
>>> unit3 = SiamObj('2', '2', a=1)
>>> unit3.connect('1', '2', 1).a = 2
>>> unit2.a == 2
True
>>> pool = unit3.pool
>>> print(len(pool))
2
>>> del unit3
>>> print(len(pool))
1


"""
from weakref import WeakKeyDictionary
from functools import reduce


class Meta(type):
    """ Adds extra method and attributes to the SiamObj class."""
    _instances = WeakKeyDictionary()

    @classmethod
    def connect(cls, *arg, **kwargs):
        for obj in cls._instances:
            keys = list(obj.__dict__.keys())
            if keys:
                temp, obj_args_values = [], []
                [temp.append(obj.__dict__[key]) for key in keys]
                for i in temp:
                    if type(i) == dict:
                        obj_args_values.append(tuple(i.values()))
                    else:
                        obj_args_values.append(i)
                param = arg + tuple(kwargs.values())
                obj_param = reduce(lambda x, y: x+y, obj_args_values)
                if param == obj_param:
                    return obj
            elif not arg and not kwargs:
                return obj
            else:
                raise AttributeError('No objects with the given attributes')

    def __call__(cls, *arg, **kwargs):
        setattr(cls, 'connect', cls.connect)
        setattr(cls, 'pool', cls._instances)

        obj = type.__call__(cls, *arg, **kwargs)
        if not cls._instances:
            cls._instances[obj] = None
            return obj
        else:
            for i in list(cls._instances):
                if i.__dict__ == obj.__dict__:
                    obj = i
                    return obj
            else:
                cls._instances[obj] = None
                return obj


class SiamObj(metaclass=Meta):
    def __init__(self, *arg, **kwargs):
        self.arg = arg
        self.kwargs = kwargs
