#!/usr/bin/env python
from history import History as H
# The set of all possible histories for a single cell.
class HistoryCloud(object):
    hs = []

    def __init__(self, **kwargs):
        self.hs = [H(i) for i in range(512)]
        if kwargs:
            self.filter(**kwargs)

    def __str__(self):
        if self.confidence is None:
            return " ??? "
        if self.confidence <= 0:
            return " ... "
        if self.confidence >= 1:
            return " ### "
        return "%0.3f" % self.confidence

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for h in self.hs:
            yield h

    def __len__(self):
        return len(self.hs)

    @property
    def NW(self):
        return [h.NW for h in self]

    @property
    def N(self):
        return [h.N for h in self]

    @property
    def NE(self):
        return [h.NE for h in self]

    @property
    def W(self):
        return [h.W for h in self]

    @property
    def E(self):
        return [h.E for h in self]

    @property
    def SW(self):
        return [h.SW for h in self]

    @property
    def S(self):
        return [h.S for h in self]

    @property
    def SE(self):
        return [h.SE for h in self]

    @property
    def confidence(self):
        if len(self) < 1:
            return None
        return float(sum([h.c for h in self])) / len(self)

    def corroborate(self, others):
        old_hs = len(self)
        [nw_n, n_n, ne_n, w_n, e_n, sw_n, s_n, se_n] = others
        comparisons = [
            (nw_n, 'SE', 'NW'), (n_n, 'S', 'N'), (ne_n, 'SW', 'NE'),
            (w_n, 'E', 'W'),                     (e_n, 'W', 'E'),
            (sw_n, 'NE', 'SW'), (s_n, 'N', 'S'), (se_n, 'NW', 'SE')]
            
        for neighbor, neighborshift, shift in comparisons:
            if neighbor is None:
                continue
            neighbor = [getattr(h, neighborshift) for h in neighbor]
            filtered = [h for h in self if getattr(h, shift) in neighbor]
            self.hs = filtered
        print old_hs - len(self)
        return old_hs - len(self)

    def filter(self, **kwargs):
        old_hs = len(self)
        for k, v in kwargs.items():
            if not self.hs:
                continue
            if not hasattr(self.hs[0], k):
                continue
            self.hs = [h for h in self.hs if getattr(h, k) == v]
        return old_hs - len(self)

if __name__ == '__main__':
    A = HistoryCloud()
