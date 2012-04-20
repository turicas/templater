#!/usr/bin/env python
# coding: utf-8

from templater import Templater


str_1 = 'my favorite color is blue'
str_2 = 'my favorite color is violet'
print 'Learning from:'
print '  ', str_1
print '  ', str_2

t = Templater() # default tolerance (0)
t.learn(str_1)
t.learn(str_2)
print 'Template for tolerance=0:'
print '  ', t._template

t = Templater(tolerance=1)
t.learn(str_1)
t.learn(str_2)
print 'Template for tolerance=1:'
print '  ', t._template
