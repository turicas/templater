Templater
=========

Given some strings, this library extracts templates from that (with the method
``learn``). Then, you can parse other strings and extract only the "movable
parts" of them based on the template created (with method ``parse``). You can
also pass these "movable parts" to fill the template and have a new string with
the same structure as others, but with data (with method ``join``).

And you have flexibility:

- If you don't want/need to ``Templater`` create the template for you, you can
  pass a pre-processed template (as a list with the tokens or as a string with
  markers).
- You can split the learning and parsing process, since the learning process
  generally is executed one time and takes a lot of time compared to parsing
  process. To turn this process handy, ``Templater`` has the methods ``dump``,
  ``save``, ``load`` and ``open``, so you can learn and save a template
  definition and later load and parse how many times you want (you can also
  load, learn more and save).


Installation
------------

`templater is available at PyPI <http://pypi.python.org/pypi/templater>`_, so
installing it is as simple as executing::

    pip install templater

Or you can download the latest version, extract and run::

    python setup.py build install


Examples
--------

All you need to know is below (and in the ``examples`` directory)::

    >>> from templater import Templater
    >>> texts_to_learn = ['<b> spam and eggs </b>', '<b> ham and spam </b>',
                          '<b> white and black </b>']
    >>> text_to_parse = texts_to_learn[-1]
    >>> template = Templater()
    >>> for text in texts_to_learn:
    ...    template.learn(text)
    ...

    >>> print 'Template created:', template._template
    Template created: [None, '<b> ', None, ' and ', None, ' </b>', None]

    >>> print 'Parsing last string:', template.parse(text_to_parse)
    Parsing last string: ['', 'white', 'black', '']

    >>> print 'Filling the blanks:', template.join(['', 'yellow', 'blue', ''])
    Filling the blanks: <b> yellow and blue </b>

You can pass pre-processed templates as a list (variable places = ``None``)::

    >>> t2 = Templater(template=[None, 'Music: ', None, ', Band: ', None])
    >>> print t2.join(['', 'Welcome to the Jungle', 'Guns and Roses'])
    Music: Welcome to the Jungle, Band: Guns and Roses

...or you can pass a string with the marker, then ``Templater`` will create the
list for you::

    >>> t3 = Templater(template='language=#,cool=#', marker='#')
    >>> print t3.join(['', 'Python', 'YES', ''])
    language=Python,cool=YES

Saving and opening templates is easy::

    >>> template.save('my-first-template.html', marker='|||')
    >>> # and some time later...
    >>> loaded_template = Templater.open('my-first-template.html', marker='|||')
    >>> print loaded_template.parse('<b> Romeo and Juliet </b>')
    ['', 'Romeo', 'Juliet', '']

The difference between ``save`` and ``dump`` is that ``save`` stores the
template string, filling the blanks with a marker and ``dump`` saves the whole
``Templater`` object with ``cPickle``. The pairs are:

- ``save`` and ``open`` (raw template string filled with marker)
- ``load`` and ``dump`` (whole object)

And to not be much literal, you can adjust tolerance too::

    >>> str_1 = 'my favorite color is blue'
    >>> str_2 = 'my favorite color is violet'
    >>> t = Templater() # default tolerance (0)
    >>> t.learn(str_1)
    >>> t.learn(str_2)
    >>> print t._template
    [None, 'my favorite color is ', None, 'l', None, 'e', None]
    >>> t = Templater(tolerance=1)
    >>> t.learn(str_1)
    >>> t.learn(str_2)
    >>> print t._template
    [None, 'my favorite color is ', None]


Author
------

This software is developed by
`Álvaro Justen aka Turicas <https://github.com/turicas>`_.

Many thanks to `Adrian Holovaty <http://www.holovaty.com/>`_ - he created
`templatemaker <http://templatemaker.googlecode.com>`_, the project which
``templater`` was inspired in/forked from.


License
-------

`GPL version 2 <http://www.gnu.org/licenses/gpl-2.0.html>`_
