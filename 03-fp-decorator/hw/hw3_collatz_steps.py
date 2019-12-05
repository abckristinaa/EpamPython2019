def collatz_steps(n):
    """ Returns quantity of steps nedeed to rich from n to 1
    according to Collatz conjecture.
    """
    assert n > 0, 'The number must be more than zero'
    return 0 if n == 1 else collatz_steps(n // 2 if n % 2 == 0 else n * 3 + 1) + 1


assert collatz_steps(16) == 4
assert collatz_steps(12) == 9
assert collatz_steps(1000000) == 152
