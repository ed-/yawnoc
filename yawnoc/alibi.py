from exceptions import Impossible
from history import History


CARDINALS = ['NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE']
OPPOSITES = ['SE', 'S', 'SW', 'E', 'W', 'NE', 'N', 'NW']


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
        alive = len([h for h in self.histories if h.c])
        return float(alive) / len(self.histories)

    def filter(self, **kwargs):
        old_total = len(self.histories)
        for key, value in kwargs.items():
            self.histories = [h for h in self.histories
                              if getattr(h, key) == value]
        if not self.histories:
            raise Impossible()
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
            if not self.histories:
                raise Impossible()
        return old_total - len(self.histories)
