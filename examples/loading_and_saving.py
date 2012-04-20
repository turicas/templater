#!/usr/bin/env python
# coding: utf-8

from templater import Templater

t = Templater()
t.learn('<b>spam</b>')
t.learn('<b>eggs</b>')
t.learn('<b>ham</b>')
t.save('my-little-template.tpl')
print t.parse('<b>parsing using first template object</b>')

t2 = Templater.load('my-little-template.tpl')
print t2.parse('<b>parsing using second template object</b>')
