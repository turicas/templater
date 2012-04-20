#!/usr/bin/env python
# coding: utf-8

from time import time
from glob import glob
from templater import Templater


files = glob('html/*.html') # You must have some .html files in html/
template = Templater()
print 'Time to learn'
start = time()
for filename in files:
    print '  Learning "%s"...' % filename,
    fp = open(filename)
    template.learn(fp.read())
    fp.close()
    print 'OK'
end = time()
print ' Time:', end - start

print 'Template created:'
print template._template

print 'Now, work!'
start = time()
for filename in files:
    print '  Parsing "%s"...' % filename
    fp = open(filename)
    print '  Result:', template.parse(fp.read())
    fp.close()
end = time()
print ' Time: ', end - start
