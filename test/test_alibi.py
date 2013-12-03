#!/usr/bin/env python
from yawnoc.alibi import History


def test_single_cells():
    for j in range(512):
        t = History(j)
        assert bool(t.bits & 256) == t.nw
        assert bool(t.bits & 128) == t.n
        assert bool(t.bits & 64) == t.ne
        assert bool(t.bits & 32) == t.w
        assert bool(t.bits & 16) == t.c
        assert bool(t.bits & 8) == t.e
        assert bool(t.bits & 4) == t.sw
        assert bool(t.bits & 2) == t.s
        assert bool(t.bits & 1) == t.se


def test_shifts():
    for j in range(512):
        t = History(j)
        assert t.bits == t.C
