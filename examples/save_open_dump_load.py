#!/usr/bin/env python
# coding: utf-8

from os import unlink
from templater import Templater


t = Templater()
t.learn('<b>spam</b>')
t.learn('<b>eggs</b>')
t.learn('<b>ham</b>')
t.save('my-little-template.html', marker='|||')
t.dump('my-template.tpl')
print t.parse('<b>parsing using first template object</b>')

t2 = Templater.open('my-little-template.html', marker='|||')
print t2.parse('<b>parsing using second template object</b>')

t3 = Templater.load('my-template.tpl')
print t3.parse('<b>parsing using third template object</b>')

# 'my-little-template.html' will have the template string with blanks filled by
# '|||'
# 'my-template.tpl' will have the pickle of Templater object

# Removing files:
unlink('my-little-template.html')
unlink('my-template.tpl')
