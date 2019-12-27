

def make_it_count(func, counter_name):
    """ Returns a new function that behave as a given function but increments
    counter_name for each сall.
    """
    def new_func(*args, **kwargs):
        globals()[counter_name] += 1
        return func(*args, **kwargs)
    return new_func


if __name__ == "__main__":
    counter_name = 0

    def my_func():
        print('Ola-la!')

    count = make_it_count(my_func, 'counter_name')
    count()
    count()
    count()
    count()
    count()
    print(counter_name)
