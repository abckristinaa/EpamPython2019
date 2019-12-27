from task1 import SiamObj


def test_passing_positional_arguments():
    object_ = SiamObj(4, 1, 8, 'a', (13, 18, 16), 'b', 438, [5, 4, [6, 8]])
    assert object_


def test_passing_keywords_arguments():
    object_ = SiamObj(zyt=48, a=15, dd='abc', b=None, m=0)
    assert object_


def test_passing_positional_and_keywords_arguments():
    object_ = SiamObj(4, 1, 8, 'a', (13, 18, 16), 'b', 438, [5, 4, [6, 8]],
                      zyt=48, a=15, dd='abc', b=None, m=0)
    assert object_


def test_passing_no_arguments():
    object_ = SiamObj()
    assert object_


def test_objects_with_same_positinal_arguments_are_the_same():
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    obj3 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    assert obj1 is obj2 is obj3


def test_objects_with_same_keyword_arguments_are_the_same():
    obj1 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    obj3 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    assert obj1 is obj2 is obj3


def test_objects_with_same_positional_and_keyword_arguments_are_the_same():
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0,mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    obj3 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    assert obj1 is obj2 is obj3


def test_objects_with_same_no_arguments_are_the_same():
    obj1 = SiamObj()
    obj2 = SiamObj()
    obj3 = SiamObj()
    assert obj1 is obj2 is obj3


def test_access_to_other_object_attributes_via_connect1():
    # if Siam class has only one object without attributes False is OK
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'ds', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    get_obj1 = obj2.connect({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a',
                            (13, 18, 16), 'b', 438, [5, 4, [6, 8]], uru=158,
                            z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                            mem={999: {888: {777: [1, 2]}}})
    assert obj1 is get_obj1


def test_connect_if_different_attr():
    # if Siam class has only one object without attributes False is OK
    obj1 = SiamObj('1', '2', b=1)
    obj2 = SiamObj('1', '2', a=1)
    obj3 = SiamObj('2', '2', a=1)
    get_obj = obj3.connect('1', '2', 1)
    assert get_obj == obj1 or obj2


def test_connect_without_attr():
    # if Siam class has only one object without attributes
    obj1 = SiamObj('1', '2', b=1)
    obj2 = SiamObj('1', '2', a=1)
    obj3 = SiamObj('2', '2', a=1)
    get_obj = obj3.connect()
    assert get_obj == obj1 or obj2


def test_set_value_to_other_object_attribute():
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'ds', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    obj2.connect({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a',
                 (13, 18, 16), 'b', 438, [5, 4, [6, 8]], uru=158,
                 z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                 mem={999: {888: {777: [1, 2]}}}).uru = 159
    assert obj1.uru == 159


def object_deletion():
    obj1 = SiamObj('First object')
    obj2 = SiamObj('First object')
    obj3 = SiamObj('Second object')
    obj4 = SiamObj('Third object')
    pool = obj3.pool
    assert len(pool) == 3
    del obj3
    assert len(pool) == 2


def test_object_deletion_if_no_attributes():
    # if Siam class has only one object without attributes False is OK
    obj1 = SiamObj('First object')
    obj2 = SiamObj('First object')
    obj3 = SiamObj('Second object')
    obj4 = SiamObj('Third object')
    pool = obj3.pool
    del obj3
    assert len(pool) == 1
