#!/usr/bin/env python
from alibi import History

def stitch(sep, *text):
    return '\n'.join(sep.join(b) for b in zip(*[a.split('\n') for a in text]))

def bit2str(b, t):
    bits = [{True: '#', False: '.'}[bool(i)] for i in 
            [b & 256, b & 128, b & 64,
             b &  32, b &  16, b &  8,
             b &   4, b &   2, b &  1]]
    if t == 0:
        return '%s %s %s\n%s %s %s\n%s %s %s' % tuple(bits)
    if t == 1:
        return '%s %s %s\n%s %s %s' % tuple(bits[-6:])
    if t == 2:
        return '%s %s\n%s %s\n%s %s' % tuple(bits[-6:])
    if t == 3:
        return '%s %s\n%s %s' % tuple(bits[-4:])


for j in range(512):
    t = History(j)
    try:
        assert t.bits == t.C, 'C was %s not %s' % (t.bits, t.C)
        assert bool(t.bits & 256) == t.nw, 'nw was %s not %s' % (t.nw, bool(t.bits & 256))
        assert bool(t.bits & 128) == t.n,  'n  was %s not %s' % (t.n,  bool(t.bits & 128))
        assert bool(t.bits &  64) == t.ne, 'ne was %s not %s' % (t.ne, bool(t.bits &  64))
        assert bool(t.bits &  32) == t.w,  'w  was %s not %s' % (t.w,  bool(t.bits &  32))
        assert bool(t.bits &  16) == t.c,  'c  was %s not %s' % (t.c,  bool(t.bits &  16))
        assert bool(t.bits &   8) == t.e,  'e  was %s not %s' % (t.e,  bool(t.bits &   8))
        assert bool(t.bits &   4) == t.sw, 'sw was %s not %s' % (t.sw, bool(t.bits &   4))
        assert bool(t.bits &   2) == t.s,  's  was %s not %s' % (t.s,  bool(t.bits &   2))
        assert bool(t.bits &   1) == t.se, 'se was %s not %s' % (t.se, bool(t.bits &   1))
    except AssertionError as ae:
        print j, ae.args

for i in range(512):
    a = History(i)
    print '===== %3i =====' % i
    print stitch('  ', bit2str(a.NW, 3), bit2str(a.N, 1), bit2str(a.NE, 3))
    print
    print stitch('  ', bit2str(a.W, 2), bit2str(a.C, 0), bit2str(a.E, 2))
    print
    print stitch('  ', bit2str(a.SW, 3), bit2str(a.S, 1), bit2str(a.SE, 3))
    print


for j in range(512):
    t = History(j)
    assert t.bits == t.C
