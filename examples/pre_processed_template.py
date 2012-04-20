#!/usr/bin/env python
# coding: utf-8

from templater import Templater

template = Templater(template=[None, '<b>', None, '</b>', None])
print template.join(['', 'Python rules', '']) # prints '<b>Python rules</b>'
