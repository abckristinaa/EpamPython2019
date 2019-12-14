""""
Реализовать контекстный менеджер, который подавляет переданные исключения
with Suppressor(ZeroDivisionError):
    1/0
print("It's fine")
"""


class Suppressor:
    def __init__(self, *excep):
        self.excep = excep

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return issubclass(exc_type, self.excep)
