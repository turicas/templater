#!/usr/bin/env python
# coding: utf-8

from cPickle import dump as pickle_dump, load as pickle_load
from _templater import longest_match as lcs


class Templater(object):
    def __init__(self, template=None, marker='|||', tolerance=0):
        self._template = template
        self._tolerance = tolerance
        if type(template) in (str, unicode):
            tokens = template.split(marker)
            self._template = list(sum(zip([None] * len(tokens), tokens), ())) \
                             + [None]

    def learn(self, new_text):
        if self._template is None:
            text = new_text
        else:
            text = '\0\0\0'.join([x for x in self._template if x is not None])
        self._template = _create_template(new_text, text, (0, len(new_text)),
                                          (0, len(text)), self._tolerance)

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
        pickle_dump(self, fp)
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
        return processed_template

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

def _create_template(str_1, str_2, (start_1, end_1), (start_2, end_2),
                     tolerance=0):
    lcs_size, lcs_1_start, lcs_2_start = lcs(str_1[start_1:end_1],
                                         str_2[start_2:end_2])
    if lcs_size <= tolerance:
        return [None]
    else:
        return _create_template(str_1, str_2,
                                (start_1, start_1 + lcs_1_start),
                                (start_2, start_2 + lcs_2_start),
                                tolerance) + \
               [str_1[start_1 + lcs_1_start:start_1 + lcs_1_start + lcs_size]] + \
               _create_template(str_1, str_2,
                                (start_1 + lcs_1_start + lcs_size, end_1),
                                (start_2 + lcs_2_start + lcs_size, end_2),
                                tolerance)
