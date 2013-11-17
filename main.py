#!/usr/bin/env python

from conway import Conway
from yawnoc import Yawnoc

from bash.colors import colorize

filename = 'random.txt'
filename = 'glider.txt'

c = Conway.load(filename)
print c

print

y = Yawnoc.load(filename)
print y

print

y.corroborate()
print y
