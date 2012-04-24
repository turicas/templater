Templater
=========

Introduction
------------

Given some strings (or files), this library extracts a common template between
them (method ``learn``) -- some people call it "reverse templating". Having
your template created, you can parse other strings/files using it - the
``parse`` method will return only what changes in this file (the "blanks"). It
does something like the opposite of what template libraries (such as
`Jinja <http://jinja.pocoo.org/>`_) do. But for now, it only can identify
fixed variables (it can't create ``for`` and ``if`` blocks, for example).

If you have the template and the "blanks" you can also fill the blanks with
the method ``join`` - it'll return a string with the template filled. There are
some other features:

- If you don't want/need to ``Templater`` (the main class) create the template
  for you, you can pass a pre-processed template (created manually or created
  before using ``learn`` and saved somewhere).
- You can split the learning and parsing process, since the learning process
  generally is executed one time and takes a lot of time compared to parsing
  process. To turn this process handy, ``Templater`` has the methods ``dump``,
  ``save``, ``load`` and ``open``, so you can learn and save a template
  definition for later loading and parsing how many times you want (you can
  also load, learn more and save).

`templater <https://github.com/turicas/templater>`_ is simple to use, easy to
learn and does the hard work for you (for example: part of the learning
algorithm is implemented in C for performance). Do you have 5 minutes? So learn
with the `Examples`_.


Installation
------------

`templater is available at PyPI <http://pypi.python.org/pypi/templater>`_, so
installing it is as simple as executing::

    pip install templater

Or you can download the latest version and install it using ``setup.py``::

    git clone https://turicas@github.com/turicas/templater.git
    cd templater
    python setup.py build install


Terminology
-----------

There are some definitions/concepts we should explicit here:

- **Template**: the whole object (instance of ``Templater``).
- **Document**: a string or file that have some kind of pattern. You'll use
  documents to make a template object learn and recognize these patterns, so
  later you can use the template object to parse a document and get only the
  information that is not "static".
- **Blocks**: the fixed parts of a template. Can change (in number and size)
  when ``learn`` is run.
- **Blanks**: also called holes or variables, blanks are the parts in a
  template that changes between documents with the same template.
- **Template definition**: the information stored in a template that defines it
  (it is a Python list with a very simple grammar that describes how the
  template is composed).
- **Markers**: when you want to save a template, something should be put
  between blocks to "mark" the blanks (so the template definition can be
  reconstructed later).
- **Named marker**: a marker plus a header is called a named marker. They are
  handy and more legible since you can access the "blanks" by names instead of
  indexes.

Doubts? Don't worry, see the `Examples`_ and you'll get it.


Examples
--------

All you need to know is below (and in the ``examples`` directory)::

    >>> from templater import Templater
    >>> documents_to_learn = ['<b> spam and eggs </b>', '<b> ham and spam </b>',
                              '<b> white and black </b>'] # list of documents
    >>> template = Templater()
    >>> for document in documents_to_learn:
    ...    template.learn(document)
    ...

    >>> print 'Template created:', template._template # template definition
    Template created: [None, '<b> ', None, ' and ', None, ' </b>', None]

    >>> document_to_parse = '<b> yellow and blue </b>'
    >>> print 'Parsing other document:', template.parse(document_to_parse)
    Parsing other document: ['', 'yellow', 'blue', '']

    >>> print 'Filling the blanks:', template.join(['', 'red', 'orange', ''])
    Filling the blanks: <b> red and orange </b>

You can pass pre-processed templates as a list (blanks are ``None``, blocks are
strings)::

    >>> t2 = Templater(template=[None, 'Music: ', None, ', Band: ', None])
    >>> print t2.join(['', 'Welcome to the Jungle', 'Guns and Roses'])
    Music: Welcome to the Jungle, Band: Guns and Roses

...or you can pass a string with markers, then ``Templater`` will create the
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

**Note**: ``save`` always add a ``\n`` to the end of file; ``load``
deletes trailing ``\r\n`` or ``\n`` in the end of file (if any).

**Note-2**: when passing a pre-processed template (using ``Templater``
initializer or ``Templater.open``) make sure it **starts and ends** with a
marker.

If you are getting a lot of blanks you can configure the learning process: just
adjust ``min_block_size`` - it's the minimum number of characters permitted to
create a new block in template::

    >>> str_1 = 'my favorite color is blue'
    >>> str_2 = 'my favorite color is violet'
    >>> t = Templater() # default min_block_size = 1
    >>> t.learn(str_1)
    >>> t.learn(str_2)
    >>> print t._template
    [None, 'my favorite color is ', None, 'l', None, 'e', None]

We don't want that ``'l'`` and ``'e'`` there, right? So::

    >>> t = Templater(min_block_size=2)
    >>> t.learn(str_1)
    >>> t.learn(str_2)
    >>> print t._template
    [None, 'my favorite color is ', None]


You can also add "headers" to your template - the headers will be the name of
your markers, so you'll have a template with named markers and ``parse`` will
return a ``dict`` instead of ``list``. It's more legible than using list
indices, let's see::

    >>> import re
    >>> # Let's create a regexp that cases with '{{var}}' (it'll be our marker)
    >>> regexp_marker = re.compile(r'{{([a-zA-Z0-9_-]*)}}')
    >>> template = Templater('{{first-var}}<b>{{second-var}}</b>{{third-var}}',
                             marker=regexp_marker)
    >>> # The template knows the name of each marker just using the regexp provided
    >>> # Passing marker as regexp to specify named markers also work for Templater.open

    >>> print template.parse('This <b> is </b> a test.')
    {'second-var': ' is ', 'third-var': ' a test.', 'first-var': 'This '}

    >>> # To save the template with named markers we need to provide a Python string.
    >>> # Templater will call .format() of this string for each marker with its name
    >>> template.save('template-with-named-markers.html', marker='--{}--')
    >>> # Will save '--first-var--<b>--second-var--</b>--third-var--\n'

And if you have a template without headers, just add to it with ``add_headers``
method::

    >>> t = Templater('+<tr><td>+</td><td>+</td></tr>+', marker='+')
    >>> t.parse('<tr><td>hello</td><td>world</td></tr>')
    ['', 'hello', 'world', '']

    >>> t.add_headers(['before', 'first-column', 'second-column', 'after'])
    >>> t.parse('<tr><td>hello</td><td>world</td></tr>')
    {'after': '', 'before': '', 'first-column': 'hello', 'second-column': 'world'}

**Note**: named markers have a problem: you can't run ``learn`` if you use them.


Notes
-----

I really want to know if you are using this project and what is your impression
about it. If you have new ideas of features, discovered bugs or just want to
say "thank you, I'm using it!", please contact me at
`alvarojusten at gmail <alvarojusten@gmail.com>`_.

If you want to code some stuff,
just `fork it on GitHub <https://github.com/turicas/templater>`_ and create a
pull request. Some technical notes for you:

- This project uses `Test-Driven Development
  <http://en.wikipedia.org/wiki/Test-Driven_Development>`_.

  - The tests are run using Python 2.7.2 on Ubuntu 11.10 amd64.
- You can see the changes between versions in
  `CHANGELOG.rst <https://github.com/turicas/templater/blob/master/CHANGELOG.rst>`_.
- This project uses `semantic versioning <http://semver.org/>`_ (thanks,
  `Tom Preston-Werner <http://tom.preston-werner.com/>`_).



Author
------

This software is developed by
`Álvaro Justen aka Turicas <http://blog.justen.eng.br/>`_.

Many thanks to `Adrian Holovaty <http://www.holovaty.com/>`_ - he created
`templatemaker <http://templatemaker.googlecode.com>`_, the project which
``templater`` was inspired in/forked from - and to
`Escola de Matemática Aplicada (Fundação Getúlio Vargas) <http://emap.fgv.br>`_
which gives me interesting problems to solve. :-)


License
-------

`GPL version 2 <http://www.gnu.org/licenses/gpl-2.0.html>`_
