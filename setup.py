#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup, Extension


setup(name='templater',
      version='0.1.0',
      description=('Extract template (a pattern) from strings and parse other'
                   'strings with this pattern.'),
      long_description=open('README.markdown').read(),
      author=u'Álvaro Justen',
      author_email='alvarojusten@gmail.com',
      url='https://github.com/turicas/templater/',
      py_modules=['templater'],
      ext_modules=[Extension('_templater', ['templater.c'])],
      keywords=['template', 'reversed template', 'template making',
                'wrapper induction'],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
