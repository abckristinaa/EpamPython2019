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


def test_objects_with_same_positinal_arguments():
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    obj3 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    assert obj1 is obj2 is obj3


def test_objects_with_same_keyword_arguments():
    obj1 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    obj3 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    assert obj1 is obj2 is obj3


def test_objects_with_same_positional_and_keyword_arguments():
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


def test_objects_with_same_no_arguments():
    obj1 = SiamObj()
    obj2 = SiamObj()
    obj3 = SiamObj()
    assert obj1 is obj2 is obj3


def test_objects_with_different_positinal_arguments():
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', '1s', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]])
    obj3 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [61, 8]])
    assert obj1 is not obj2
    assert obj1 is not obj3


def test_objects_with_different_keyword_arguments():
    obj1 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd1', 45), a=0,
                   mem={999: {888: {777: [1, 2]}}})
    obj3 = SiamObj(uru=158, z=[1, 2, 3], tr=None, auto=(12, 'dsd', 45), a=0,
                   mem={999: {888: {777: [1, 2, 3]}}})
    assert obj1 is not obj2
    assert obj1 is not obj3


def test_objects_with_different_positional_and_keyword_arguments():
    obj1 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0,mem={999: {888: {777: [1, 2]}}})
    obj2 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 21, 3], tr=None,
                   auto=(12, 'dsd', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    obj3 = SiamObj({1: [158, 'a', 4], '1': ('vc', 'ds', 0)}, 'a', (13, 18, 16),
                   'b', 438, [5, 4, [6, 8]], uru=158, z=[1, 2, 3], tr=None,
                   auto=(12, '1dsd', 45), a=0, mem={999: {888: {777: [1, 2]}}})
    assert obj1 is not obj2
    assert obj1 is not obj3


def test_access_to_other_object_attributes_via_connect():
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
