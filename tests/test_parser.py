#!/usr/bin/env python
# coding: utf-8

from templater import _parser


def test_parsing_template_with_one_blank():
    text = '<b> testing </b>'
    template = [None]
    result = _parser(template, text)
    expected = [text]
    assert result == expected

def test_parsing_template_with_three_blanks():
    text = '<b> testing </b>'
    template = [None, '<b> ', None, ' </b>', None]
    result = _parser(template, text)
    expected = ['', 'testing', '']
    assert result == expected

def test_parsing_four_blanks():
    text = '<b> testing and programming </b>'
    template = [None, '<b> ', None, ' and ', None, ' </b>', None]
    result = _parser(template, text)
    expected = ['', 'testing', 'programming', '']
    assert result == expected

def test_parsing_non_parseable_text_should_raise_ValueError():
    text = '<b> testing programming </b>'
    template = ['<b> ', None, ' and ', None, ' </b>']
    try:
        result = _parser(template, text)
    except ValueError:
        pass
    else:
        assert 'ValueError not raised!' == False

def test_parsing_last_blank():
    text = '<b> testing and programming </b>blah'
    template = [None, '<b> ', None, ' and ', None, ' </b>', None]
    result = _parser(template, text)
    expected = ['', 'testing', 'programming', 'blah']
    assert result == expected

def test_parsing_first_blank():
    text = 'blah<b> testing and programming </b>'
    template = [None, '<b> ', None, ' and ', None, ' </b>', None]
    result = _parser(template, text)
    expected = ['blah', 'testing', 'programming', '']
    assert result == expected
