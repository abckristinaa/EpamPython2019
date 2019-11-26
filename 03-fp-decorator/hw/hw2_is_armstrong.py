def is_armstrong(number):
    """ Returns True if the given number is Armstrong number, else False.
    """
    return True if number == sum(map(lambda x: int(x) ** len(str(number)),
                                     str(number))) else False


assert is_armstrong(153) == True, 'Число Армстронга'
assert is_armstrong(10) == False, 'Не число Армстронга'