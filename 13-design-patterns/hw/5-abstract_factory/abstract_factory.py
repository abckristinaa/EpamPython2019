"""
Представьте, что вы пишите программу по формированию и выдачи комплексных обедов для сети столовых, которая стала
расширяться и теперь предлагает комплексные обеды для вегетарианцев, детей и любителей китайской кухни.

С помощью паттерна "Абстрактная фабрика" вам необходимо реализовать выдачу комплексного обеда, состоящего из трёх
позиций (первое, второе и напиток).
В файле menu.yml находится меню на каждый день, в котором указаны позиции и их принадлежность к
определенному типу блюд.
"""
from abc import ABC, abstractmethod
import yaml


class AbstractMeal(ABC):
    @abstractmethod
    def first_course(self) -> str:
        pass

    @abstractmethod
    def second_course(self) -> str:
        pass

    @abstractmethod
    def drink(self) -> str:
        pass

    @staticmethod
    def title() -> str:
        pass


class VeganMeal(AbstractMeal):
    def first_course(self) -> str:
        return menu[today]['first_courses']['vegan']

    def second_course(self) -> str:
        return menu[today]['second_courses']['vegan']

    def drink(self) -> str:
        return menu[today]['drinks']['vegan']

    @staticmethod
    def title():
        return 'vegan:'


class ChildMeal(AbstractMeal):
    def first_course(self) -> str:
        return menu[today]['first_courses']['child']

    def second_course(self) -> str:
        return menu[today]['second_courses']['child']

    def drink(self) -> str:
        return menu[today]['drinks']['child']

    @staticmethod
    def title():
        return 'child:'


class ChineseMeal(AbstractMeal):
    def first_course(self) -> str:
        return menu[today]['first_courses']['chinese']

    def second_course(self) -> str:
        return menu[today]['second_courses']['chinese']

    def drink(self) -> str:
        return menu[today]['drinks']['chinese']

    @staticmethod
    def title():
        return 'chinese:'


class AbstractFactory(ABC):
    @abstractmethod
    def create_complex_lunch(self) -> AbstractMeal:
        pass


class VeganLunchFactory(AbstractFactory):
    def create_complex_lunch(self) -> VeganMeal:
        return VeganMeal()


class ChildLunchFactory(AbstractFactory):
    def create_complex_lunch(self) -> ChildMeal:
        return ChildMeal()


class ChineseLunchFactory(AbstractFactory):
    def create_complex_lunch(self) -> ChineseMeal:
        return ChineseMeal()


def client_code(factory: AbstractFactory) -> None:
    meal = factory.create_complex_lunch()
    first = meal.first_course()
    second = meal.second_course()
    drink = meal.drink()
    title = meal.title()
    print(f"Комплексный обед {title}\n"
          f"first meal: {first}\n"
          f"second meal: {second}\n"
          f"drink: {drink}\n")


if __name__ == '__main__':
    with open("menu.yml", 'r') as file:
        menu = yaml.safe_load(file)
        today = input('День недели: ')
        client_code(VeganLunchFactory())
        client_code(ChildLunchFactory())
        client_code(ChineseLunchFactory())
