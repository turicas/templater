#!/usr/bin/env python
# coding: utf-8

from templater import _create_template


def test_template_creation_0():
    str_1 = '1'
    str_2 = '2'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None]
    assert result == expected

def test_template_creation():
    str_1 = 'a1'
    str_2 = 'a2'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, 'a', None]
    assert result == expected

def test_template_creation_2():
    str_1 = 'ab1'
    str_2 = 'ab2'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, 'ab', None]
    assert result == expected

def test_template_creation_3():
    str_1 = '1a'
    str_2 = '2a'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, 'a', None]
    assert result == expected

def test_template_creation_4():
    str_1 = 'abcdef'
    str_2 = 'qbedff'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, 'b', None, 'd', None, 'f', None]
    assert result == expected

def test_template_creation_5():
    str_1 = 'abcccc'
    str_2 = 'abe'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, 'ab', None]
    assert result == expected

def test_template_creation_6():
    str_1 = 'ccccab'
    str_2 = 'eab'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, 'ab', None]
    assert result == expected

def test_equal_strings_should_return_one_element():
    str_1 = '<b> asd </b>'
    str_2 = '<b> asd </b>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> asd </b>', None]
    assert result == expected

def test_different_strings_with_same_size():
    str_1 = '<b> asd </b>'
    str_2 = '<b> qwe </b>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> ', None, ' </b>', None]
    assert result == expected

def test_different_strings_with_different_size():
    str_1 = '<b> asd </b>'
    str_2 = '<b> qwe123 </b>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> ', None, ' </b>', None]
    assert result == expected

def test_different_strings_with_one_of_size_zero():
    str_1 = '<b> asd </b>'
    str_2 = '<b>  </b>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> ', None, ' </b>', None]
    assert result == expected

def test_more_than_one_variable_with_same_size():
    str_1 = '<b> asd </b><u> 123 </u>'
    str_2 = '<b> qwe </b><u> 456 </u>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> ', None, ' </b><u> ', None, ' </u>', None]
    assert result == expected

def test_more_than_one_variable_with_different_sizes():
    str_1 = '<b> asdfgh </b><u> 123 </u>'
    str_2 = '<b> qwe </b><u> 456qwe </u>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> ', None, ' </b><u> ', None, ' </u>', None]
    assert result == expected

def test_tolerance():
    str_1 = 'my favorite color is blue'
    str_2 = 'my favorite color is violet'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)),
                              tolerance=0)
    expected = [None, 'my favorite color is ', None, 'l', None, 'e', None]
    assert result == expected

    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)),
                              tolerance=1)
    expected = [None, 'my favorite color is ', None]
    assert result == expected
