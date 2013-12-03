#!/usr/bin/env python

def cat(*bits):
    # Concatenate an unknown number of bits and return an integer.
    r = 0
    for b in bits:
        r <<= 1
        if b:
            r += int(b)
    return r

CARDINALS = ['NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE']
OPPOSITES = ['SE', 'S', 'SW', 'E', 'W', 'NE', 'N', 'NW']


class History(object):
    # A cell and its neighborhood. The center cell's next state is property Z.
    bits = None

    def __init__(self, bits):
        self.bits = bits & 511

    # Each of the nine individual cells.
    @property
    def nw(self):
        return bool(self.bits & 256)

    @property
    def n(self):
        return bool(self.bits & 128)

    @property
    def ne(self):
        return bool(self.bits & 64)

    @property
    def w(self):
        return bool(self.bits & 32)

    @property
    def c(self):
        return bool(self.bits & 16)

    @property
    def e(self):
        return bool(self.bits & 8)

    @property
    def sw(self):
        return bool(self.bits & 4)

    @property
    def s(self):
        return bool(self.bits & 2)

    @property
    def se(self):
        return bool(self.bits & 1)

    @property
    def Z(self):
        # The next state the center cell will be.
        neighbors = sum([self.nw, self.n, self.ne,
                        self.w,          self.e,
                        self.sw, self.s, self.se])
        return (self.c, neighbors) in [(True, 2), (True, 3), (False, 3)]

    # The eight shift operations.
    @property
    def NW(self):
        return cat(self.nw, self.n,
                   self.w,  self.c)

    @property
    def N(self):
        return cat(self.nw, self.n, self.ne,
                   self.w,  self.c, self.e)

    @property
    def NE(self):
        return cat(self.n, self.ne,
                   self.c, self.e)
    @property
    def W(self):
        return cat(self.nw, self.n,
                   self.w,  self.c,
                   self.sw, self.s)

    @property
    def C(self):
        return cat(self.nw, self.n, self.ne,
                   self.w,  self.c, self.e,
                   self.sw, self.s, self.se)

    @property
    def E(self):
        return cat(self.n, self.ne,
                   self.c, self.e,
                   self.s, self.se)

    @property
    def SW(self):
        return cat(self.w,  self.c,
                   self.sw, self.s)

    @property
    def S(self):
        return cat(self.w,  self.c, self.e,
                   self.sw, self.s, self.se)

    @property
    def SE(self):
        return cat(self.c, self.e,
                   self.s, self.se)


class Alibi(object):
    # The set of all possible Histories for a single cell.
    histories = []

    def __init__(self, **kwargs):
        self.histories = [History(i) for i in range(512)]
        if kwargs:
            self.filter(**kwargs)

    # The eight aggregate shift operations.
    @property
    def NW(self):
        return [h.NW for h in self.histories]

    @property
    def N(self):
        return [h.N for h in self.histories]

    @property
    def NE(self):
        return [h.NE for h in self.histories]

    @property
    def W(self):
        return [h.W for h in self.histories]

    @property
    def E(self):
        return [h.E for h in self.histories]

    @property
    def SW(self):
        return [h.SW for h in self.histories]

    @property
    def S(self):
        return [h.S for h in self.histories]

    @property
    def SE(self):
        return [h.SE for h in self.histories]

    @property
    def confidence(self):
        if not self.histories:
            return None
        alive = len([h for h in self.histories if h.c])
        return float(alive) / len(self.histories)

    def filter(self, **kwargs):
        old_total = len(self.histories)
        for key, value in kwargs.items():
            self.histories = [h for h in self.histories
                              if getattr(h, key) == value]
        return old_total - len(self.histories)

    def guess(self, tolerance=0.0):
        if self.confidence <= tolerance:
            return self.filter(c=False)
        if 1.0 - self.confidence <= tolerance:
            return self.filter(c=True)
        return 0

    def corroborate(self, neighbors):
        old_total = len(self.histories)
        neighborhood = zip(neighbors, OPPOSITES, CARDINALS)
            
        for neighbor, nshift, cshift in neighborhood:
            if neighbor is None:
                continue
            nshifted = set(getattr(neighbor, nshift))
            self.histories = [h for h in self.histories
                              if getattr(h, cshift) in nshifted]
        return old_total - len(self.histories)
