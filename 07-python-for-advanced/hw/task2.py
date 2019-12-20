"""
Написать свое property c кэшем и таймаутом
полностью повторяет поведение стандартной property за исключением:
    * хранит результат работы метода некоторое время, которое передается
      параметром в инициализацию проперти
    * пересчитывает значение, если таймер истек
"""
import time
import uuid


def timer_property(t):

    class t_property:

        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")

            if not hasattr(obj, '_msg'):
                setattr(obj, 'expired', time.ctime(time.time() + t))
                return self.fget(obj)
            else:
                if obj.__dict__['expired'] <= time.ctime():
                    obj.__dict__['expired'] = time.ctime()
                    return self.fget(obj)
                else:
                    return obj.__dict__['_msg']

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            if not value:
                delattr(obj, '_msg')
                delattr(obj, 'expired')
            else:
                self.fset(obj, value)
                obj.__dict__['expired'] = time.ctime()

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        def getter(self, fget):
            return type(self)(fget, self.fset, self.fdel, self.__doc__)

        def setter(self, fset):
            return type(self)(self.fget, fset, self.fdel, self.__doc__)

        def deleter(self, fdel):
            return type(self)(self.fget, self.fset, fdel, self.__doc__)

    return t_property


class Message:

    @timer_property(t=10)
    def msg(self):
        self._msg = self.get_message()
        return self._msg

    @msg.setter # reset timer also
    def msg(self, param):
        self._msg = param

    def get_message(self):
        """
        Return random string
        """
        return uuid.uuid4().hex


if __name__ == '__main__':
    m = Message()
    initial = m.msg
    assert initial is m.msg
    time.sleep(10)
    assert initial is not m.msg
