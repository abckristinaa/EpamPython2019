"""
Реализовать класс Quaternion, позволяющий работать с кватернионами
https://ru.wikipedia.org/wiki/%D0%9A%D0%B2%D0%B0%D1%82%D0%B5%D1%80%D0%BD%D0%B8%D0%BE%D0%BD
Функциональность (магическими методами):
- V сложение
- V умножение
- деление
- V сравнение
- V нахождение модуля
- V строковое представление и repr
По желанию:
- взаимодействие с числами других типов
"""
import numpy as np


class Quaternion:
    """ Returns quaternion object Quaternion(q0, q1, q2, q3) which are:
    q0 - scalar part
    q1, q2, q3 - vector part (coordinates x, y, z)
    """
    def __init__(self, scal=0, xpos=0, ypos=0, zpos=0):
        self.scal = scal
        self.vector = np.array([xpos, ypos, zpos])

    def __eq__(self, other):
        if isinstance(other, Quaternion):
            return all(self.vector == other.vector) and self.scal == other.scal
        else:
            raise TypeError('Operation between given types is not supported')

    def __lt__(self, other):
        if isinstance(other, Quaternion):
            return all(self.vector < other.vector)
        else:
            raise TypeError('Operation between given types is not supported')

    def __gt__(self, other):
        if isinstance(other, Quaternion):
            return all(self.vector > other.vector)
        else:
            raise TypeError('Operation between given types is not supported')

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.scal + other.scal,
                              *(self.vector + other.vector))
        else:
            raise TypeError('Operation between given types is not supported')

    def __iadd__(self, other):
        return self + other

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.scal * other, *(self.vector * other))
        else:
            raise TypeError('Operation between given types is not supported')

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.scal * other, *(self.vector * other))

        elif isinstance(other, Quaternion):
            x, y, z = self.vector[0], self.vector[1], self.vector[2]
            ox, oy, oz = other.vector[0], other.vector[1], other.vector[2]

            if self.scal == other.scal == 0:
                return Quaternion(-x * ox - y * oy - z * oz,
                                  y * oz - z * oy,
                                  z * ox - x * oz,
                                  x * oy - y * ox)

            elif y == oy == z == oz == 0:
                return Quaternion(self.scal * other.scal - x * ox,
                                  self.scal * ox + x * other.scal, 0, 0)
            else:
                return Quaternion(
                    self.scal * other.scal - x * ox - y * oy - z * oz,
                    self.scal * ox + x * other.scal + y * oz - z * oy,
                    self.scal * oy - x * oz + y * other.scal + z * ox,
                    self.scal * oz + x * oy - y * ox + z * other.scal)
        else:
            raise TypeError('Operation between given types is not supported')

    def __imul__(self, other):
        if isinstance(other, (int, float)):
            return self * other

    def __truediv__(self, other):
        if isinstance(other, Quaternion):
            i = other.scal ** 2 + sum(_ ** 2 for _ in other.vector)
            if i > 0:
                return self * Quaternion(other.scal/i,
                                         *[-(_ / i) for _ in other.vector])
            else:
                raise ZeroDivisionError("division by zero")
        else:
            raise TypeError('Operation between given types is not supported')

    def __abs__(self):
        return sum(self.vector ** 2, self.scal ** 2) ** 0.5

    def __str__(self):
        return f"Quaternion({self.scal}, {', '.join(map(str, self.vector))})"

    def __repr__(self):
        return f"Quaternion({self.scal}, {repr(self.vector)})"


if __name__ == "__main__":
    empty = Quaternion()
    print(empty)  # Quaternion(0, 0, 0, 0)
    print(repr(empty))  # Quaternion(0, array([0, 0, 0]))

    q1 = Quaternion(2, 2, 5, 8)
    q2 = Quaternion(2, 2, 5, 8)
    q3 = Quaternion(30,-15, 3, 16)
    q4 = Quaternion(25, 32, 15, 8)
    q5 = Quaternion(25, 32, 15, 9)
    print(q1)  # Quaternion(2, 2, 5, 8)
    print(q3)  # Quaternion(30, -15, 3, 16)

    assert (q3 == q2) == False
    assert (q1 == q2) == True

    assert (q2 < q5) == True
    assert (q4 < q5) == False
    assert (q3 > q2) == False
    assert (q5 > q2) == True

    assert (q1 + q2) == Quaternion(4, 4, 10, 16)

    q1 += Quaternion(1, 1, 1, 0)
    assert q1 == Quaternion(3, 3, 6, 8)

    assert q1 * q2 == Quaternion(-94, 20, 19, 43)
    assert q1 * 2 == Quaternion(6, 6, 12, 16)
    assert 2 * q1 == Quaternion(6, 6, 12, 16)

    q2 *= 2
    assert q2 == Quaternion(4, 4, 10, 16)

    assert (Quaternion(-94, 20, 19, 43) / Quaternion(2, 2, 5, 8)) == q1

    assert abs(Quaternion(5, 5, 4, 3)) == 8.660254037844387
    assert abs(Quaternion(5, 5, 5, 5)) == 10
