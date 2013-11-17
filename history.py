#!/usr/bin/env python
# A single possible past state of a cell and its neighbors.
class History(object):
    x = None

    def __init__(self, data=None):
        self.x = 0 if data is None else (data % 512)

    def __str__(self):
        #return str(self.x)
        r = '%1d%1d%1d\n%1d%1d%1d -> %d\n%1d%1d%1d'
        return r % (self.nw, self.n, self.ne,
                    self.w,  self.c, self.e, self.Z,
                    self.sw, self.s, self.se)

    def __repr__(self):
        return str(self)

    def sum(self, v):
        z = [265, 128, 64, 32, 16, 8, 4, 2, 1][-len(v):]
        return sum([i * j for i, j in zip(v, z)])

    @property
    def nw(self):
        return 1 if self.x & 256 else 0

    @property
    def n(self):
        return 1 if self.x & 128 else 0

    @property
    def ne(self):
        return 1 if self.x & 64 else 0

    @property
    def w(self):
        return 1 if self.x & 32 else 0

    @property
    def c(self):
        return 1 if self.x & 16 else 0

    @property
    def e(self):
        return 1 if self.x & 8 else 0

    @property
    def sw(self):
        return 1 if self.x & 4 else 0

    @property
    def s(self):
        return 1 if self.x & 2 else 0

    @property
    def se(self):
        return 1 if self.x & 1 else 0

    @property
    def Z(self):
        ns = sum([self.nw, self.n, self.ne,
                  self.w,          self.e,
                  self.sw, self.s, self.se])
        if self.c:
            return 1 if ns in [2, 3] else 0
        return 1 if ns in [3] else 0

    @property
    def NW(self):
        return self.sum([self.nw, self.n,
                         self.w,  self.c])

    @property
    def N(self):
        return self.sum([self.nw, self.n, self.ne,
                         self.w,  self.c, self.e])

    @property
    def NE(self):
        return self.sum([self.n, self.ne,
                          self.c, self.e])
    @property
    def W(self):
        return self.sum([self.nw, self.n,
                         self.w,  self.c,
                         self.sw, self.s])

    @property
    def E(self):
        return self.sum([self.n, self.ne,
                         self.c, self.e,
                         self.s, self.se])

    @property
    def SW(self):
        return self.sum([self.w,  self.c,
                         self.sw, self.s])

    @property
    def S(self):
        return self.sum([self.w,  self.c, self.e,
                         self.sw, self.s, self.se])

    @property
    def SE(self):
        return self.sum([self.c, self.e,
                         self.s, self.se])

if __name__ == '__main__':
    from random import randint
    for i in range(512):
        h = History(i)
        if h.Z:
            print h
            print
