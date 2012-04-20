#!/usr/bin/env python
# coding: utf-8

from templater import Templater


texts_to_learn = ['<b> spam and eggs </b>', '<b> ham and spam </b>',
                  '<b> white and black </b>']
text_to_parse = texts_to_learn[-1]
template = Templater()
for text in texts_to_learn:
    print 'Learning "%s"...' % text
    template.learn(text)
print 'Template created:', template._template
print 'Parsing text "%s"...' % text_to_parse
print '  Result:', template.parse(text_to_parse)
print 'Filling the blanks:', template.join(['', 'yellow', 'blue', ''])
