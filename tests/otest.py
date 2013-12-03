#!/usr/bin/env python


def cat(*bits):
    # Concatenate an unknown number of bits and return an integer.
    r = 0
    for b in bits:
        r <<= 1
        if b:
            r += int(b)
    return r

for i in range(512):
    j = [i & 256, i & 128, i & 64,
         i &  32, i &  16, i &  8,
         i &   4, i &   2, i &   1]
    j = [bool(x) for x in j]
    k = [int(x) for x in j]
    try:
        assert i == cat(*j), 'Expected %3i, got %3i from %s' % (i, cat(*j), k)
    except AssertionError as ae:
        print ae

