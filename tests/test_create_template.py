#!/usr/bin/env python
# coding: utf-8

from templater import _create_template


def test_different_strings_should_return_one_blank():
    str_1 = '1'
    str_2 = '2'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None]
    assert result == expected

def test_equal_strings_should_return_one_block():
    str_1 = '<b> asd </b>'
    str_2 = '<b> asd </b>'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected = [None, '<b> asd </b>', None]
    assert result == expected

def test_different_strings_with_same_size():
    str_1 = 'a1'
    str_2 = 'a2'
    result_1 = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected_1 = [None, 'a', None]
    assert result_1 == expected_1

    str_1 = '1a'
    str_2 = '2a'
    result_2 = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected_2 = [None, 'a', None]
    assert result_2 == expected_2

    str_1 = '<b> asd </b>'
    str_2 = '<b> qwe </b>'
    result_3 = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)))
    expected_3 = [None, '<b> ', None, ' </b>', None]
    assert result_3 == expected_3

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

def test_min_block_size():
    str_1 = 'my favorite color is blue'
    str_2 = 'my favorite color is violet'
    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)),
                              min_block_size=1)
    expected = [None, 'my favorite color is ', None, 'l', None, 'e', None]
    assert result == expected

    result = _create_template(str_1, str_2, (0, len(str_1)), (0, len(str_2)),
                              min_block_size=2)
    expected = [None, 'my favorite color is ', None]
    assert result == expected
