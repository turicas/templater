#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup, Extension


setup(name='templater',
      version='0.1.0',
      description=('Extract template (a pattern) from strings and parse other'
                   'strings with this pattern.'),
      author=u'Álvaro Justen',
      author_email='alvarojusten@gmail.com',
      py_modules=['templater'],
      ext_modules=[Extension('_templater', ['templater.c'])],
)
