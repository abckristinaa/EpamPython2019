def letters_range(start, stop=None, step=1, **kwargs):
    """ Returns a list of letters from [start] to [stop]
    with a given step (default step is 1). The step mustn't be zero.
    Takes a dictionary with the values to substitute original alphabet"""

    alphabet = {index: i for index, i
                in enumerate("abcdefghijklmnopqrstuvwxyz")}
    if kwargs:
        for k in kwargs:
            alphabet.update(tuple((index, kwargs[k])
                                  for index, i in alphabet.items() if i == k))

    start = [index for index, i in alphabet.items() if i == start][0]
    result = []

    if stop is None:
        stop = 0
        while start > stop:
            result.append(alphabet[stop])
            stop += step
    else:
        stop = [index for index, i in alphabet.items() if i == stop][0]
        if step > 0:
            while stop > start:
                result.append(alphabet[start])
                start += step
        elif step < 0:
            while stop < start:
                result.append(alphabet[start])
                start += step
        else:
            print('argument 3 must not be zero')
            return
    return result


letters_range('z', 'g', -2, **{'v': 666})
