#!/usr/bin/env python
# coding: utf-8

from os import unlink
from re import compile as re_compile
from templater import Templater, MARKER, NAMED_MARKER


regexp_marker = re_compile(r'{{([a-zA-Z0-9_-]*)}}')

def read_file_and_delete(filename):
    fp = open(filename)
    contents = fp.read()
    fp.close()
    unlink(filename)
    return contents

def write_file(filename, contents):
    fp = open(filename, 'w')
    fp.write(contents)
    fp.close()

def test_new_learn_text_trying_to_delete_some_variable():
    template = Templater()
    template.learn('<b> a and b </b>')
    template.learn('<b> c and d </b>')
    template.learn('<b> e and  </b>')
    result = template._template
    expected = [None, '<b> ', None, ' and ', None, ' </b>', None]
    assert result == expected
    #TODO: should never have less variables when learning?

def test_parse():
    template = Templater()
    template.learn('a b d')
    template.learn('a e d')
    result = template.parse('a b c d')
    expected = ['', 'b c', '']
    assert result == expected

def test_join():
    template = Templater()
    template.learn('a b d')
    template.learn('a e d')
    parsed = template.parse('a b c d')
    result = template.join(parsed)
    expected = 'a b c d'
    assert result == expected

def test_join_with_less_parameters_than_variables_should_raise_ValueError():
    template = Templater()
    template.learn('a b d')
    template.learn('a e d')
    try:
        result = template.join([''])
    except ValueError:
        pass
    else:
        assert 'ValueError not raised!' == False

def test_Templater_should_import_pre_processed_template_if_user_want():
    pre_processed = [None, '<u>', None, '</u>', None]
    template = Templater(template=pre_processed)
    assert template._template == pre_processed
    assert template.join(['', 'python', '']) == '<u>python</u>'

def test_Templater_should_import_template_string_with_marks():
    template = Templater(template='<b>|||</b>', marker='|||')
    result_template = template._template
    assert result_template == [None, '<b>', None, '</b>', None]
    assert template.join(['', 'spam eggs', '']) == '<b>spam eggs</b>'

def test_Templater_should_load_and_save_templates_from_and_to_files():
    processed_template = [None, '<b>', None, '</b><u>', None, '</u>', None]
    template = Templater(template=processed_template, tolerance=5)
    template.dump('my-template.tpl')
    t2 = Templater.load('my-template.tpl')
    unlink('my-template.tpl')
    result_1 = t2._template
    expected_1 = processed_template
    result_2 = t2._tolerance
    expected_2 = 5
    assert expected_1 == result_1
    assert expected_2 == result_2

def test_Templater_should_be_able_to_adjust_tolerance():
    t = Templater(tolerance=1)
    t.learn('git and pyth')
    t.learn('eggs and spam')
    expected = [None, ' and ', None]
    result = t._template
    assert expected == result

def test_Templater_save_should_save_template_as_a_raw_file_with_markers():
    processed_template = [None, '<b>', None, '</b><u>', None, '</u>', None]
    t = Templater(template=processed_template)
    t.save('test.html', marker='|||')
    result = read_file_and_delete('test.html')
    expected = '|||<b>|||</b><u>|||</u>|||'
    assert expected == result

def test_Templater_should_accept_named_markers_in_init():
    template = '{{start}}<b>{{middle}}</b>{{end}}'
    t = Templater(template=template, marker=regexp_marker)
    result_1 = t._template
    expected_1 = [None, '<b>', None, '</b>', None]
    assert expected_1 == result_1

    result_2 = t._headers
    expected_2 = ['start', 'middle', 'end']
    assert expected_2 == result_2

def test_Templater_open_should_load_template_from_a_raw_file_with_markers():
    write_file('test.html', '|||<b>|||</b><u>|||</u>|||')
    t = Templater.open('test.html', marker='|||')
    unlink('test.html')
    result = t._template
    expected = [None, '<b>', None, '</b><u>', None, '</u>', None]
    assert expected == result

def test_named_markers_should_work():
    write_file('test.html',
               '|||[first]<b>|||[second]</b><u>|||[third]</u>|||[fourth]')
    t = Templater.open('test.html', marker=re_compile(r'\|\|\|\[([^\]]+)\]'))
    unlink('test.html')
    result_1 = t._template
    expected_1 = [None, '<b>', None, '</b><u>', None, '</u>', None]
    assert result_1 == expected_1

    result_2 = t.parse('<b>hello</b><u>world</u>')
    expected_2 = {'first': '', 'second': 'hello', 'third': 'world',
                  'fourth': ''}
    assert expected_2 == result_2

def test_should_not_have_named_marks_without_nothing_in_the_middle():
    write_file('test.html', '{{first}}{{second}}<u>{{text}}</u>{{last}}')
    try:
        t = Templater.open('test.html', marker=regexp_marker)
    except ValueError:
        pass
    else:
        assert "ValueError not raised!" == False

def test_if_there_are_no_named_marker_in_the_start_of_template():
    write_file('test.html', '<u>{{text}}</u>{{end}}')
    try:
        t = Templater.open('test.html', marker=regexp_marker)
    except ValueError:
        unlink('test.html')
    else:
        unlink('test.html')
        assert "ValueError not raised!" == False

def test_raise_ValueError_if_there_is_no_named_marker_in_the_end_of_template():
    write_file('test.html', '{{start}}<u>{{text}}</u>')
    try:
        t = Templater.open('test.html', marker=regexp_marker)
    except ValueError:
        unlink('test.html')
    else:
        unlink('test.html')
        assert "ValueError not raised!" == False

# SAVE: marker + headers cases:
# marker | self._named_markers | result
#     NO |                  NO | self._marker    / ignore headers
#     NO |                 YES | NAMED_MARKER    / headers or self._headers
#    YES |                  NO | marker          / ignore headers
#    YES |                 YES | marker.format() / headers or self._headers

def test_save_should_use_self_marker_if_no_marker_supplied():
    t = Templater(template='+<u>+</u>+', marker='+')
    t.save('test.html')
    result = read_file_and_delete('test.html')
    expected = '+<u>+</u>+'
    assert expected == result

def test_save_should_use_NAMED_MARKER_if_template_has_named_markers_and_no_marker_supplied():
    t = Templater(template='{{one}}<u>{{two}}</u>{{three}}',
                  marker=regexp_marker)
    t.save('test.html')
    result = read_file_and_delete('test.html')
    named_markers = [NAMED_MARKER.format(header) for header in t._headers]
    expected = t.join(named_markers)
    assert expected == result

def test_save_should_use_marker_if_supplied_and_template_hasnt_named_markers():
    t = Templater(template='+<u>+</u>+', marker='+')
    t.save('test.html', marker='%%')
    result = read_file_and_delete('test.html')
    expected = '%%<u>%%</u>%%'
    assert expected == result

def test_save_should_use_python_format_if_marker_is_supplied_and_template_has_named_markers():
    t = Templater(template='{{start}}<u>{{text}}</u>{{end}}',
                  marker=regexp_marker)
    t.save('test.html', marker='[--{}--]')
    result = read_file_and_delete('test.html')
    expected = '[--start--]<u>[--text--]</u>[--end--]'
    assert expected == result

def test_save_should_use_headers_instead_of_self_headers_if_supplied():
    t = Templater(template='{{one}}<u>{{two}}</u>{{three}}',
                  marker=regexp_marker)
    t.save('test.html', headers=list('abc'))
    result_1 = read_file_and_delete('test.html')
    named_markers = [NAMED_MARKER.format(header) for header in list('abc')]
    expected_1 = t.join(named_markers)
    assert expected_1 == result_1

    t.save('test.html', marker='[--{}--]', headers=list('abc'))
    result_2 = read_file_and_delete('test.html')
    expected_2 = '[--a--]<u>[--b--]</u>[--c--]'
    assert expected_2 == result_2

def test_passing_headers_with_different_size_from_self_headers_should_raise_AttributeError():
    t = Templater(template='{{one}}<u>{{two}}</u>{{three}}',
                  marker=regexp_marker)
    try:
        t.save('test.html', headers=list('abcde'))
    except AttributeError:
        pass
    else:
        unlink('test.html')
        raise 'AttributeError not raised!'

def test_template_with_named_markers_should_not_be_able_to_learn():
    t = Templater(template='{{one}}<u>{{two}}</u>{{three}}',
                  marker=regexp_marker)
    try:
        t.learn('a<u>b</u>c')
    except NotImplementedError:
        pass
    else:
        print t._template
        assert 'NotImplementedError not raised' == False

def test_should_be_able_to_add_headers_to_a_template_without_named_markers():
    t = Templater(template='|||<u>|||</u>|||', marker='|||')
    t.add_headers(['one', 'two', 'three'])
    result = t.parse('a<u>b</u>c')
    expected = {'one': 'a', 'two': 'b', 'three': 'c'}
    assert result == expected

def test_add_headers_should_raise_ValueError_if_number_of_blanks_differ_from_number_of_headers():
    t = Templater(template='|||<u>|||</u>|||', marker='|||')
    try:
        t.add_headers(['one', 'two', 'three', 'four'])
    except ValueError:
        pass
    else:
        assert 'ValueError not raised!' == False
