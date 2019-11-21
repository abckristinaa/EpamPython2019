def letters_range(start, stop=None, step=1, **kwargs):
    """ Returns a list of letters from [start] to [stop]
    with a given step (default step is 1). The step mustn't be zero.
    Takes a dictionary with the values to substitute original alphabet"""

    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    start = alphabet.index(start)

    if kwargs:
        for k in kwargs:
            idx = alphabet.index(k)
            alphabet[idx] = str(kwargs[k])

    if stop is None:
        result = list(alphabet[0:start:step])
    else:
        stop = alphabet.index(stop)
        if not step:
            print('argument 3 must not be zero')
            return
        else:
            result = list(alphabet[start:stop:step])

    return result


print(letters_range('z', 'a', -3, **{'q': 666, 'e': 80}))
