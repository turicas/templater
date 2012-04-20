#!/usr/bin/env python
# coding: utf-8

from cPickle import dump as pickle_dump, load as pickle_load
from _templater import longest_match as lcs


class Templater(object):
    def __init__(self, template=None, marker='|||'):
        self._template = template
        if type(template) in (str, unicode):
            tokens = template.split(marker)
            self._template = list(sum(zip([None] * len(tokens), tokens), ())) \
                             + [None]

    def learn(self, new_text):
        if self._template is None:
            text = new_text
        else:
            text = '\0\0\0'.join([x for x in self._template if x is not None])
        self._template = _create_template(new_text, text)

    def parse(self, text):
        return _parser(self._template, text)

    def join(self, elements):
        elements_length = len(elements)
        variables_length = self._template.count(None)
        if elements_length != variables_length:
            error_msg = ("Wrong number of variables (passwd: {}, expected: "
                         "{})".format(elements_length, variables_length))
            raise ValueError(error_msg)
        text = self._template[:]
        variable_index = 0
        for index, element in enumerate(text):
            if element is None:
                text[index] = elements[variable_index]
                variable_index += 1
        return ''.join(text)

    def save(self, filename):
        """Save the template to file ``filename`` so you can re-use it later.

        This method uses cPickle to serialize internal template model, so you
        don't need to pass through the learn process everytime you need to
        parse data. It's worth using this method since learning process
        generally cost a lot of time compared to parsing.
        """
        fp = open(filename, 'w')
        pickle_dump(self._template, fp)
        fp.close()

    @staticmethod
    def load(filename):
        """Load a template from ``filename``, return ``Templater`` object.

        This method must be used in pair with ``Templater.save`` - it loads
        the template definition from a file using cPickle, creates a
        ``Templater`` object with the definition and returns it.
        """
        fp = open(filename)
        processed_template = pickle_load(fp)
        fp.close()
        return Templater(template=processed_template)

def _parser(template, text):
    last_element_index = len(template) - 1
    result = []
    text_index = 0
    for index, element in enumerate(template):
        if element is None:
            if index != last_element_index:
                new_index = text.index(template[index + 1], text_index)
            else:
                new_index = last_element_index
            result.append(text[text_index:new_index])
            text_index = new_index
        else:
            element_length = len(element)
            assert text[text_index:text_index + element_length] == element
            text_index += element_length
    return result

def template_iterative(s1, s2):
    result = []
    insert = 0
    start_1, end_1 = 0, len(s1)
    start_2, end_2 = 0, len(s2)
    while True:
        size, s1start, s2start = lcs(s1[start_1:end_1], s2[start_2:end_2])
        string_to_add = s1[start_1 + s1start:start_1 + s1start + size]
        if string_to_add:
            add_to_result = [
                    ((start_1, start_1 + s1start), (start_2, start_2 + s2start)),
                    string_to_add,
                    ((start_1 + s1start + size, end_1), (start_2 + s2start + size, end_2))]
        else:
            add_to_result = [None]
        result[insert:insert + 1] = add_to_result
        continue_processing = False
        for index, element in enumerate(result):
            if type(element) == tuple:
                next_to_process = element
                start_1, end_1 = element[0]
                start_2, end_2 = element[1]
                insert = index
                continue_processing = True
                break
        if not continue_processing:
            break
    return result

def template_recursive(s1, s2):
    size, s1start, s2start = lcs(s1, s2)
    if size == 0:
        return [None]
    return template_recursive(s1[:s1start], s2[:s2start]) + \
            [s1[s1start:s1start + size]] + \
            template_recursive(s1[s1start + size:], s2[s2start + size:])

_create_template = template_recursive
