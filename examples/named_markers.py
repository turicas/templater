#!/usr/bin/env python
# coding: utf-8

from re import compile as re_compile
from templater import Templater


regexp_marker = re_compile(r'{{([a-zA-Z0-9_-]*)}}') # match ''{{var}}''
template = Templater('{{first-var}}<b>{{second-var}}</b>{{third-var}}',
                     marker=regexp_marker)
# regexp marker also works for Templater.open to specify named markers
result = template.parse('This <b> is </b> a test.') # returns a dict
print result

template.save('template-with-named-markers.html', marker='{{{{{}}}}}')
