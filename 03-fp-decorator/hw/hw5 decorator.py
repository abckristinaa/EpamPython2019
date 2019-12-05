from functools import wraps
from functools import reduce
from time import perf_counter


calls = 0
perf_time_ms = 0


def decorator(calls, perf_time_ms):
    """ Returns a tuple with common number of function calls
    and common time of evalueting in milliseconds.
    """

    calls = 0
    perf_time_ms = 0

    def deco(func):
        @wraps(func)
        def inner(*args, **kwargs):

            global calls
            global perf_time_ms

            calls += 1
            start = perf_counter() * 1000
            func(*args, **kwargs)
            perf_time_ms = perf_counter() * 1000 - start
            return calls, perf_time_ms
        return inner
    return deco


@decorator(calls, perf_time_ms)
def fib_rec(n):
    """ Implementation using recursion. """
    if n > 2:
        return fib_rec(n - 1) + fib_rec(n - 2)
    else:
        return 1


@decorator(calls, perf_time_ms)
def fib_loop(n):
    """ Implementation using a loop. """
    a = 0
    b = 1
    for __ in range(n):
        a, b = b, a + b
    return a


@decorator(calls, perf_time_ms)
def fib_dict(n):
    """ Implementation using a dictionary as a storage for every number."""
    cache = {0: 0, 1: 1}
    if n not in cache:
        for i in range(2, n + 1):
            cache[i] = (cache[i-1] + cache[i - 2])
    return cache[n]


@decorator(calls, perf_time_ms)
def fib_reduce(n):
    return reduce(lambda a, b: a + [a[-1] + a[-2]], range(n), [1, 1])[-1]


n = 4
fib_rec(n)
print(calls, perf_time_ms)

fib_loop(n)
print(calls, perf_time_ms)

fib_dict(n)
print(calls, perf_time_ms)

fib_reduce(n)
print(calls, perf_time_ms)
