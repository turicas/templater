Templater
=========

Given some strings, this library extracts templates from that (with the method
`learn`). Then, you can parse other strings and extract only the "movable
parts" of them based on the template created (with method `parse`). You can
also pass these "movable parts" to fill the template and have a new string with
the same structure as others, but with data (with method `join`).

And you have flexibility: if you don't want/need to `Templater` create the
template for you, you can pass a pre-processed template (as a list with the
tokens or as a string with markers).

Examples
--------

All you need to know is below (and in the `examples` directory):

    >>> from templater import Templater
    >>> texts_to_learn = ['<b> spam and eggs </b>', '<b> ham and spam </b>',
                          '<b> white and black </b>']
    >>> text_to_parse = texts_to_learn[-1]
    >>> template = Templater()
    >>> for text in texts_to_learn:
    ...    template.learn(text)

    >>> print 'Template created:', template._template
    Template created: [None, '<b> ', None, ' and ', None, ' </b>', None]

    >>> print 'Parsing last string:', template.parse(text_to_parse)
    Parsing last string: ['', 'white', 'black', '']

    >>> print 'Filling the blanks:', template.join(['', 'yellow', 'blue', ''])
    Filling the blanks: <b> yellow and blue </b>

    >>> t2 = Templater(template=[None, 'Music: ', None, ', Band: ', None])
    >>> print t2.join(['', 'Welcome to the Jungle', 'Guns and Roses'])
    Music: Welcome to the Jungle, Band: Guns and Roses

    >>> t3 = Templater(template='language=#,cool=#', marker='#')
    >>> print t3.join(['', 'Python', 'YES', ''])
    language=Python,cool=YES


License
-------

[GPL version 2](http://www.gnu.org/licenses/gpl-2.0.html)
