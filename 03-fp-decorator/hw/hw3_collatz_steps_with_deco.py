def make_count(func):
    """Counts the number of calls for given function. Return a number.
    """
    counter = -1

    def inner(n):
        nonlocal counter
        func(n)
        counter += 1
        return counter
    return inner


@make_count
def collatz_steps(n):
    """Checks the given number for Collatz conjecture.
    """
    assert n > 0, 'The number must be more than zero'
    return n if n == 1 else collatz_steps(n // 2 if n % 2 == 0 else n * 3 + 1)

print(collatz_steps(1000000))
