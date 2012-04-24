#!/usr/bin/env python
# coding: utf-8

from cPickle import dump as pickle_dump, load as pickle_load
from re import compile as re_compile
from _templater import longest_match as lcs


type_regexp = type(re_compile(''))
MARKER = '|||'
NAMED_MARKER = '{{{{{}}}}}' # '{{sample-var}}'

class Templater(object):
    def __init__(self, template=None, marker='|||', min_block_size=1):
        self._template = template
        self._min_block_size = min_block_size
        self._marker = marker
        self._headers = None
        self._named_markers = False
        if type(template) in (str, unicode):
            self._template, self._named_markers, self._headers = \
                    _create_template_from_string(template, marker)

    def learn(self, new_text):
        if self._named_markers:
            raise NotImplementedError("Actually you can't learn in a template "
                                      "with named markers")
        if self._template is None:
            text = new_text
        else:
            text = '\0\0\0'.join(filter(lambda x: x is not None, self._template))
        self._template = _create_template(new_text, text, (0, len(new_text)),
                                          (0, len(text)), self._min_block_size)

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
            error_msg = ("Wrong number of variables (passed: {}, expected: "
                         "{})".format(elements_length, variables_length))
            raise AttributeError(error_msg)
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

    def save(self, filename, marker=None, headers=None):
        """Save the template to ``filename`` using ``marker`` as marker.

        This method looks like ``Templater.dump``, the difference is that it
        does not save/pickle the entire ``Templater`` object - it uses
        ``Templater.join`` to fill the blanks with ``marker`` and then save the
        resulting string to ``filename``.
        It should be used in pair with ``Templater.open``.
        """
        if not self._named_markers:
            if marker is None:
                marker = self._marker
            blanks = [marker] * self._template.count(None)
        else:
            if headers is not None and len(headers) != len(self._headers):
                raise AttributeError('Incorrect number of headers (passed:'
                                     ' {}, expected: {})'.format(
                                     len(headers), len(self._headers)))
            if marker is None:
                marker = NAMED_MARKER
            if headers is None:
                headers = self._headers
            blanks = [marker.format(header) for header in headers]
        fp = open(filename, 'w')
        fp.write(self.join(blanks) + '\n')
        fp.close()

    @staticmethod
    def open(filename, marker=MARKER):
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
        if contents[-2:] == '\r\n':
            contents = contents[:-2]
        elif contents[-1] == '\n':
            contents = contents[:-1]
        template = Templater(template=contents, marker=marker)
        return template

    def add_headers(self, headers):
        """Add/modifiy headers (names of markers) to a template."""
        if len(headers) != self._template.count(None):
            raise ValueError("Wrong number of headers (passed: {}, expected: "
                             "{})".format(len(headers), self._template.count(None)))
        self._named_markers = True
        self._headers = headers

    def parse_file(self, filename):
        """Open, read a file and call ``Templater.parse`` with its contents.

        If the file ends with ``\n`` or ``\r\n``, it'll be removed.
        """
        fp = open(filename)
        contents = fp.read()
        fp.close()
        if contents[-2:] == '\r\n':
            contents = contents[:-2]
        elif contents[-1] == '\n':
            contents = contents[:-1]
        return self.parse(contents)


def _parser(template, text):
    result = []
    text_index = 0
    last_element_index = len(template) - 1
    for index, element in enumerate(template):
        if element is None:
            if index != last_element_index:
                new_index = text.index(template[index + 1], text_index)
            else:
                new_index = None
            result.append(text[text_index:new_index])
            text_index = new_index
        else:
            element_length = len(element)
            assert text[text_index:text_index + element_length] == element
            text_index += element_length
    return result

def _create_template(str_1, str_2, (start_1, end_1), (start_2, end_2),
                     min_block_size=1):
    lcs_size, lcs_1_start, lcs_2_start = lcs(str_1[start_1:end_1],
                                         str_2[start_2:end_2])
    if lcs_size < min_block_size:
        return [None]
    else:
        common = str_1[start_1 + lcs_1_start:start_1 + lcs_1_start + lcs_size]
        return _create_template(str_1, str_2,
                                (start_1, start_1 + lcs_1_start),
                                (start_2, start_2 + lcs_2_start),
                                min_block_size) + \
               [str_1[start_1 + lcs_1_start:start_1 + lcs_1_start + lcs_size]] + \
               _create_template(str_1, str_2,
                                (start_1 + lcs_1_start + lcs_size, end_1),
                                (start_2 + lcs_2_start + lcs_size, end_2),
                                min_block_size)

def _create_template_from_string(text, marker):
    named_markers = type(marker) == type_regexp
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
        return template, True, headers
    return template, False, None
