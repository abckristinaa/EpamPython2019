import time

import pytest

from task2 import Message


@pytest.yield_fixture
def obj():
    """ Creates an instance of Message class for all tests"""
    m = Message()
    yield m
    del m


def test_returning_value_is_string(obj):
    return_type = type(obj.msg)
    expected = str
    assert return_type == expected


def test_returning_value_length_is_32char(obj):
    return_lenght = len(obj.msg)
    expected = 32
    assert return_lenght == expected


def test_first_call_to_msg(obj):
    initial = obj.msg
    assert initial == obj.msg


def test_attribute_msg_is_registered(obj):
    obj.msg
    attributes = obj.__dict__
    assert '_msg' in attributes


def test_attribute_expired_is_registered(obj):
    obj.msg
    attributes = obj.__dict__
    assert 'expired' in attributes


def test_expired_attr_calculation_is_correct_with_time_10(obj):
    expected_time = time.ctime(time.time() + 10)
    obj.msg
    object_time = obj.__dict__['expired']
    assert expected_time == object_time


def test_second_call_within_10_sec_returns_cached_value(obj):
    first_call = obj.msg
    second_call = obj.msg
    assert first_call == second_call


def test_series_of_calls_within_10_sec_return_first_cached_value(obj):
    first = obj.msg
    second = obj.msg
    third = obj.msg
    fourth = obj.msg
    assert first == second == third == fourth


def test_returning_new_value_after_given_time(obj):
    first_call = obj.msg
    time.sleep(10)
    after_time_call = obj.msg
    assert first_call != after_time_call


def test_attributes_deleted_when_time_reset(obj):
    obj.msg
    attributes_registered = list(obj.__dict__)
    obj.msg = 0
    attributes_deleted = list(obj.__dict__)
    assert len(attributes_registered) == 2
    assert not attributes_deleted
