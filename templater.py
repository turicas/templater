#!/usr/bin/env python
# coding: utf-8

from cPickle import dump as pickle_dump, load as pickle_load
from _templater import longest_match as lcs


class Templater(object):
    def __init__(self, template=None, marker='|||', tolerance=0):
        self._template = template
        self._tolerance = tolerance
        self._marker = marker
        self._named_markers = False
        if type(template) in (str, unicode):
            self._template = _create_template_from_string(template, marker)

    def learn(self, new_text):
        if self._template is None:
            text = new_text
        else:
            text = '\0\0\0'.join(filter(lambda x: x is not None, self._template))
        self._template = _create_template(new_text, text, (0, len(new_text)),
                                          (0, len(text)), self._tolerance)

    def parse(self, text):
        result = _parser(self._template, text)
        if self._named_markers:
            return dict(zip(self._headers, result))
        else:
            return result

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

    def dump(self, filename):
        """Dump the template object to ``filename`` so you can re-use it later.

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

        This method must be used in pair with ``Templater.dump`` - it loads
        the template definition from a file using cPickle, creates a
        ``Templater`` object with the definition and returns it.
        """
        fp = open(filename)
        processed_template = pickle_load(fp)
        fp.close()
        return processed_template

    def save(self, filename, marker=None):
        """Save the template to ``filename`` using ``marker`` as marker.

        This method looks like ``Templater.dump``, the difference is that it
        does not save/pickle the entire ``Templater`` object - it uses
        ``Templater.join`` to fill the blanks with ``marker`` and then save the
        resulting string to ``filename``.
        It should be used in pair with ``Templater.open``.
        """
        if marker is None:
            marker = self._marker
        blanks = [marker for x in self._template if x is None]
        fp = open(filename, 'w')
        fp.write(self.join(blanks))
        fp.close()

    @staticmethod
    def open(filename, marker='|||', named_markers=False):
        """Open ``filename``, split in ``marker``, return ``Templater`` object.

        You should use this method in pair with ``Templater.save`` or if you
        want to write the templates with your own hands. It works similar to
        ``Templater.load``, except by the fact that ``load`` saves the entire
        ``Templater`` object and ``open`` saves only the template string,
        filling the blanks with ``marker``.
        """
        fp = open(filename)
        contents = fp.read()
        fp.close()
        if not named_markers:
            template = _create_template_from_string(contents, marker, False)
            headers = None
        else:
            template, headers = _create_template_from_string(contents, marker,
                                                             True)
        t = Templater(template=template, marker=marker)
        t._headers = headers
        t._named_markers = named_markers
        return t


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
        common = str_1[start_1 + lcs_1_start:start_1 + lcs_1_start + lcs_size]
        return _create_template(str_1, str_2,
                                (start_1, start_1 + lcs_1_start),
                                (start_2, start_2 + lcs_2_start),
                                tolerance) + \
               [common] + \
               _create_template(str_1, str_2,
                                (start_1 + lcs_1_start + lcs_size, end_1),
                                (start_2 + lcs_2_start + lcs_size, end_2),
                                tolerance)

def _create_template_from_string(text, marker, named_markers=False):
    if named_markers:
        results = marker.split(text)
        tokens, headers = [x for x in results[::2] if x], results[1::2]
    else:
        tokens = [x for x in text.split(marker) if x != '']
    template = list(sum(zip([None] * len(tokens), tokens), ())) + [None]
    if named_markers:
        if template.count(None) != len(headers):
            raise ValueError("Template error! Verify if markers are separated"
                             " at least by one character")
        return template, headers
    return template
