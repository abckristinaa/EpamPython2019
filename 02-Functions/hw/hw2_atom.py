def atom(a=None):
    """ Returns 4 functions as API for: getting, setting,
    processing and deleting the value of a variable.
    Default value is None.
    """

    def get_value():
        return a

    def set_value(value):
        nonlocal a
        a = value
        print(f"New value is {value}")
        return

    def delete_value():
        nonlocal a
        a = None
        print("Value was reset to None")
        return

    def process_value(*func):
        nonlocal a
        for i in func:
            a = i(a)
        return a

    return get_value, set_value, process_value, delete_value


gval, sval, pval, dval = atom(32)
