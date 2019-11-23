def make_it_count(func, counter_name):
    """ Returns a new function that behave as given function but increments
    counter_name for each сall.
    """

    def new_func():
        global counter_name
        counter_name += 1
        return func()

    return new_func()
