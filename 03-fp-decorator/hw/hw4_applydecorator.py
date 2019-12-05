
def applydecorator(func):
    """ Makes a decorator from the given function. """
    def inner(f, *args, **kwargs):
        func(f, *args, **kwargs)
        f = helper(f)
        return f
    return inner


def helper(f):
    def inner(*args, **kwargs):
        return f(*args, **kwargs)
    return inner


@applydecorator
def saymyname(f, *args, **kwargs):
    print('Name is', f.__name__)
    return f(*args, **kwargs)


# saymyname is now a decorator
@saymyname
def foo(*whatever):
    return whatever
