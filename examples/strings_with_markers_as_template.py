#!/usr/bin/env python
# coding: utf-8

from templater import Templater


template = Templater(template='<b>||| and |||</b>', marker='|||')
print template.join(['', 'red', 'blue', '']) # prints '<b>red and blue</b>'
