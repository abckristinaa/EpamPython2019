

def make_it_count(counter_name):
    """ Returns a new function that behave as a given function but increments
    counter_name for each сall.
    """
    def inner(func):
        def new_func(*args, **kwargs):
            globals()['counter_name'] += 1
            return func(*args, **kwargs)
        return new_func
    return inner


if __name__ == "__main__":
    counter_name = 0

    @make_it_count(counter_name)
    def my_func():
        print('Ola-la!')


    my_func()
    my_func()
    my_func()
    my_func()
    print(counter_name)
