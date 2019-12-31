"""
С помощью паттерна "Цепочка обязанностей" составьте список покупок для выпечки блинов.
Необходимо осмотреть холодильник и поочередно проверить, есть ли у нас необходимые ингридиенты:
    2 яйца
    300 грамм муки
    0.5 л молока
    100 грамм сахара
    10 мл подсолнечного масла
    120 грамм сливочного масла

В итоге мы должны получить список недостающих ингридиентов.
"""
from abc import ABC, abstractmethod
from typing import Union


ingredients: list = ['eggs', 'flour', 'milk', 'sugar',
                     'sunflower_oil', 'butter']
amount_: list = [2, 300, 0.5, 100, 10, 120]
RECIPE = dict(zip(ingredients, amount_))


class Handler(ABC):
    """ Abstract base class for Handlers. """
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    """ Defines default behavior for handlers. """

    _next_handler: Handler = None

    def set_next(self, handler: Handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class Fridge:
    """ Defines methods for refrigerator and stores food. """

    food: list
    amount: list
    name: str

    def __init__(self, food: list, amount: list = None):
        if amount is None:
            self.food: dict = dict.fromkeys(food, 0)
        else:
            self.food: dict = dict(zip(food, amount))

    def add_food(self, name: str, amount: Union[int, float]):
        self.food[name] = self.food.get([name], 0) + amount

    def take_food(self, name: str, amount: Union[int, float]):
        if name in self.food:
            if self.food[name] >= amount:
                self.food[name] -= amount
            else:
                self.food[name] = 0


class EggsHandler(AbstractHandler):
    def handle(self, fridge: Fridge, product='eggs'):
        if fridge.food[product] <= RECIPE[product]:
            print(f"To buy: {RECIPE[product] - fridge.food[product]} {product}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class FlourHandler(AbstractHandler):
    def handle(self, fridge: Fridge, product='flour'):
        if fridge.food[product] <= RECIPE[product]:
            print(f"To buy: {RECIPE[product] - fridge.food[product]} {product}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class MilkHandler(AbstractHandler):
    def handle(self, fridge: Fridge, product='milk'):
        if fridge.food[product] <= RECIPE[product]:
            print(f"To buy: {RECIPE[product] - fridge.food[product]} {product}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class SugarHandler(AbstractHandler):
    def handle(self, fridge: Fridge, product='sugar'):
        if fridge.food[product] <= RECIPE[product]:
            print(f"To buy: {RECIPE[product] - fridge.food[product]} {product}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class SunflowerOilHandler(AbstractHandler):
    def handle(self, fridge: Fridge, product='sunflower_oil'):
        if fridge.food[product] <= RECIPE[product]:
            print(f"To buy: {RECIPE[product] - fridge.food[product]} {product}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class ButterHandler(AbstractHandler):
    def handle(self, fridge: Fridge, product='butter'):
        if fridge.food[product] <= RECIPE[product]:
            print(f"To buy: {RECIPE[product] - fridge.food[product]} {product}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


def check_ingredients(fridge: Fridge):
    eggs = EggsHandler()
    flour = FlourHandler()
    milk = MilkHandler()
    sugar = SugarHandler()
    sunflower_oil = SunflowerOilHandler()
    butter = ButterHandler()

    eggs.set_next(flour).set_next(milk).set_next(sugar).set_next(
        sunflower_oil).set_next(butter)

    eggs.handle(fridge)


if __name__ == '__main__':
    print("-" * 20)
    print("Fridge is empty: ")
    print("-" * 20)
    fridge = Fridge(ingredients)
    check_ingredients(fridge)

    print("-"*20)
    print("Fridge is half empty: ")
    print("-" * 20)
    fridge2 = Fridge(ingredients, amount=[5, 100, 0.3, 50, 500, 300])
    check_ingredients(fridge2)
