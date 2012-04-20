#!/usr/bin/env python
# coding: utf-8

from templater import _create_template


def test_template_creation_0():
    result = _create_template('1', '2')
    expected = [None]
    assert result == expected

def test_template_creation():
    result = _create_template('a1', 'a2')
    expected = [None, 'a', None]
    assert result == expected

def test_template_creation_2():
    result = _create_template('ab1', 'ab2')
    expected = [None, 'ab', None]
    assert result == expected

def test_template_creation_3():
    result = _create_template('1a', '2a')
    expected = [None, 'a', None]
    assert result == expected

def test_template_creation_4():
    result = _create_template('abcdef', 'qbedff')
    expected = [None, 'b', None, 'd', None, 'f', None]
    assert result == expected

def test_template_creation_5():
    result = _create_template('abcccc', 'abe')
    expected = [None, 'ab', None]
    assert result == expected

def test_template_creation_6():
    result = _create_template('ccccab', 'eab')
    expected = [None, 'ab', None]
    assert result == expected

def test_equal_strings_should_return_one_element():
    result = _create_template('<b> asd </b>', '<b> asd </b>')
    expected = [None, '<b> asd </b>', None]
    assert result == expected

def test_different_strings_with_same_size():
    result = _create_template('<b> asd </b>', '<b> qwe </b>')
    expected = [None, '<b> ', None, ' </b>', None]
    assert result == expected

def test_different_strings_with_different_size():
    result = _create_template('<b> asd </b>', '<b> qwe123 </b>')
    expected = [None, '<b> ', None, ' </b>', None]
    assert result == expected

def test_different_strings_with_one_of_size_zero():
    result = _create_template('<b> asd </b>', '<b>  </b>')
    expected = [None, '<b> ', None, ' </b>', None]
    assert result == expected

def test_more_than_one_variable_with_same_size():
    result = _create_template('<b> asd </b><u> 123 </u>', '<b> qwe </b><u> 456 </u>')
    expected = [None, '<b> ', None, ' </b><u> ', None, ' </u>', None]
    assert result == expected

def test_more_than_one_variable_with_different_sizes():
    result = _create_template('<b> asdfgh </b><u> 123 </u>', '<b> qwe </b><u> 456qwe </u>')
    expected = [None, '<b> ', None, ' </b><u> ', None, ' </u>', None]
    assert result == expected
