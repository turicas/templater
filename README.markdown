Templater
=========

Given some strings, this library extracts templates from that (with the method
`learn`). Then, you can parse other strings and extract only the "movable
parts" of them based on the template created (with method `parse`). You can
also pass these "movable parts" to fill the template and have a new string with
the same structure as others, but with data (with method `join`).

Example
-------

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

License
-------

[GPL version 2](http://www.gnu.org/licenses/gpl-2.0.html)
