"""
В этом задании будем улучшать нашу систему классов из задания прошлой лекции
(Student, Teacher, Homework)
Советую обратить внимание на defaultdict из модуля collection для
использования как общую переменную
1. Как то не правильно, что после do_homework мы возвращаем все тот же
объект - будем возвращать какой-то результат работы (HomeworkResult)
HomeworkResult принимает объект автора задания, принимает исходное задание
и его решение в виде строки
Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'
    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания
2. Если задание уже просрочено хотелось бы видеть исключение при do_homework,
а не просто принт 'You are late'.
Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.
3. Student и Teacher имеют одинаковые по смыслу атрибуты
(last_name, first_name) - избавиться от дублирования с помощью наследования
4.
Teacher
Атрибут:
    homework_done - структура с интерфейсом как в словаря, сюда поподают все
    HomeworkResult после успешного прохождения check_homework
    (нужно гаранитровать остутствие повторяющихся результатов по каждому
    заданию), группировать по экземплярам Homework.
    Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
Методы:
    check_homework - принимает экземпляр HomeworkResult и возвращает True если
    ответ студента больше 5 символов, так же при успешной проверке добавить в
    homework_done.
    Если меньше 5 символов - никуда не добавлять и вернуть False.
    reset_results - если передать экземпряр Homework - удаляет только
    результаты этого задания из homework_done, если ничего не передавать,
    то полностью обнулит homework_done.
PEP8 соблюдать строго, проверку делаю автотестами и просмотром кода.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""

import datetime as dt
from collections import defaultdict


class DeadlineError(Exception):
    """Raised when deadline is out."""


class Homework:
    """Sets text, created, deadline attributes.
    is_active method returns True if deadline isn't out, else False."""
    def __init__(self, text, deadline):
        self.text = text
        self.created = dt.datetime.now()
        self.deadline = dt.timedelta(days=deadline)

    def is_active(self):
        return (self.created + self.deadline) > dt.datetime.now()


class HomeworkResult:
    """ Sets homework, created, solution, author attributes."""
    def __init__(self, student, homework: Homework, solution: str):
        if not isinstance(homework, Homework):
            raise TypeError('You gave a not Homework object')
        self.homework = homework
        self.created = dt.datetime.now()
        self.solution = solution
        self.author = student


class Person:
    """Base class for Student and Teacher. Sets first_name and last_name."""
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Student(Person):
    """Provides do_homework method for Student instances.

    do_homework method takes Homework instance and solution and returns
    HomeworkResult object if deadline is not out else raises DeadlineError."""
    def do_homework(self, homework: Homework, solution: str):
        if homework.is_active():
            return HomeworkResult(self, homework, solution)
        else:
            raise DeadlineError("You are late")


class Teacher(Person):
    """Provides some homework processing methods for Teacher instances.

    Class attribute homework_done stores Homework objects as keys and unique
    solutions as values. Homework_done is common for all teachers.

    Methods:
    create_homework - takes textand deadline(days) and returns Homework object
    check_homework - takes HomeworkResult object and returns True if
                    solution length > 5 letters, else False
    reset_results - creates an empty homework_done if no Homework object is
                    given, else delete Homework object key.
                    """
    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text, days_to_work):
        return Homework(text, days_to_work)

    @classmethod
    def check_homework(cls, res: HomeworkResult):
        if len(res.solution) > 5:
            cls.homework_done[res.homework].add(res.solution)
            return True
        else:
            return False

    @classmethod
    def reset_results(cls, homework=None):
        if homework:
            del cls.homework_done[homework]
        else:
            cls.homework_done = defaultdict(set)


if __name__ == '__main__':
    opp_teacher = Teacher('Daniil', 'Shadrin')
    advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

    lazy_student = Student('Roman', 'Petrov')
    good_student = Student('Lev', 'Sokolov')

    oop_hw = opp_teacher.create_homework('Learn OOP', 1)
    docs_hw = opp_teacher.create_homework('Read docs', 5)

    result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
    result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
    result_3 = lazy_student.do_homework(docs_hw, 'done')
    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except Exception:
        print('There was an exception here')
    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done
    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print(Teacher.homework_done[oop_hw])
    Teacher.reset_results()
