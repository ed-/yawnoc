#!/usr/bin/env python
# Yawnoc tries to work Conway backwards.
from alibi import Alibi
from alibi import Impossible


class GardenOfEden(Exception):
    # Board appears to be impossible to get to from anywhere.
    pass


class BadGuess(Exception):
    # Guess we made a poor assumption along the way.
    pass


class Yawnoc(object):
    def __init__(self, conway):
        self.cells = [[Alibi(Z=cell)
                       for cell in row]
                      for row in conway.cells]
        self._oob = {}

    def __str__(self):
        return self.confstr

    @property
    def rows(self):
        return len(self.cells)

    @property
    def columns(self):
        if not self.cells:
            return 0
        return len(self.cells[0])

    @property
    def confidence(self):
        return [[cell.confidence
                 for cell in row]
                for row in self.cells]

    @property
    def bestguess(self):
        return [[cell.confidence >= 0.5
                 for cell in row]
                for row in self.cells]

    @property
    def confstr(self):
        return '\n'.join(' '.join('%0.3f' % cell for cell in row)
                         for row in self.confidence)

    @property
    def span(self):
        return [[len(cell.histories)
                 for cell in row]
                for row in self.cells]

    @property
    def spanstr(self):
        return '\n'.join(' '.join(('%3i' % cell) for cell in row)
                         for row in self.span)

    def cell_at(self, row, column):
        try:
            return self.cells[row][column]
        except IndexError:
            # Assume all cells out of bounds are always dead.
            oob = Alibi(Z=False)
            if (row, column) in self._oob:
                return self._oob[(row, column)]
            if row < 0:
                oob.filter(nw=False, n=False, ne=False)
            if row >= self.rows:
                oob.filter(sw=False, s=False, se=False)
            if column < 0:
                oob.filter(nw=False, w=False, sw=False)
            if column >= self.columns:
                oob.filter(ne=False, e=False, se=False)
            # Memoize the result, it won't change.
            self._oob[(row, column)] = oob
            return oob

    def neighbors(self, row, column):
        r, c = row, column
        cardinals = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                     (r, c - 1), (r, c + 1),
                     (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
        return [self.cell_at(r, c) for (r, c) in cardinals]

    def corroborate(self, debug=False):
        total_removed = 0
        removed = None
        while removed != 0:
            removed = 0
            for r in range(self.rows):
                for c in range(self.columns):
                    neighbors = self.neighbors(r, c)
                    try:
                        culled = self.cell_at(r, c).corroborate(neighbors)
                        removed += culled
                        if debug and culled:
                            print self
                            print
                    except Impossible:
                        raise GardenOfEden()
            total_removed += removed
        return total_removed

    def guess(self, debug=False):
        for r in range(self.rows):
            for c in range(self.columns):
                culled = self.cell_at(r, c).guess(0.25)
                if culled:
                    try:
                        self.corroborate(debug=debug)
                    except GardenOfEden:
                        # Let's assume it was a bad guess.
                        raise BadGuess()
                if debug and culled:
                    print self
                    print
