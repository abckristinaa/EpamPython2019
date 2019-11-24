import inspect
from itertools import chain


def modified_func(func, *fixated_args, **fixated_kwargs):
    def new_function(*args, **kwargs):
        nonlocal fixated_args, fixated_kwargs

        if len(args):
            fixated_args = tuple(chain(fixated_args, args))
        if len(kwargs):
            fixated_kwargs = dict(list(fixated_kwargs.items()) +
                                  list(kwargs.items()))
        return func(*fixated_args, **fixated_kwargs)

    new_function.__name__ = func.__name__
    new_function.__doc__ = \
"""A func implementation of {0} with pre-applied arguments being:
{1}
source_code:
{2}
""".format(func.__name__, inspect.getcallargs(func), inspect.getsource(func))
    return new_function
