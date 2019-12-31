"""
Используя паттерн "Декоратор" реализуйте возможность дополнительно добавлять к кофе
    маршмеллоу, взбитые сливки и сироп, а затем вычислить итоговую стоимость напитка.
"""
from abc import ABC, abstractmethod


class Component(ABC):
    """ Base class. """
    @abstractmethod
    def get_cost(self):
        raise NotImplementedError("Override get_cost method")


class Base_Decorator(Component):
    """ Base class decorator for adding ingridients. """
    def __init__(self, coffee):
        self.coffee = coffee

    def get_cost(self):
        return self.coffee.get_cost()


class Whip(Base_Decorator):
    """ Adds cost for the Whip. """
    def __init__(self, coffe):
        super().__init__(coffe)

    def get_cost(self):
        return self.coffee.get_cost() + 0.5


class Marshmallow(Base_Decorator):
    """ Adds cost for the Marshmallow. """
    def __init__(self, coffe):
        super().__init__(coffe)

    def get_cost(self):
        return self.coffee.get_cost() + 0.75


class Syrup(Base_Decorator):
    """ Adds cost for the Syrup. """
    def __init__(self, coffe):
        super().__init__(coffe)

    def get_cost(self):
        return self.coffee.get_cost() + 0.25


class BaseCoffe(Component):
    def get_cost(self):
        return 90


if __name__ == "__main__":
    coffe = BaseCoffe()
    coffe = Whip(coffe)
    coffe = Marshmallow(coffe)
    coffe = Syrup(coffe)
    print("Итоговая стоимость за кофе: {}".format(str(coffe.get_cost())))
