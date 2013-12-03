#!/usr/bin/env python
# Yawnoc tries to work Conway backwards.
from alibi import Alibi

class Yawnoc(object):
    def __init__(self, conway):
        self.cells = [[Alibi(Z=cell)
                       for cell in row]
                      for row in conway.cells]
        self._oob = {}

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

    def cell_at(self, row, column):
        try:
            return self.cells[row][column]
        except IndexError:
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
            self._oob[(row, column)] = oob
            return oob

    def neighbors(self, row, column):
        r, c = row, column
        cardinals = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                     (r    , c - 1),             (r    , c + 1),
                     (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
        return [self.cell_at(r, c) for (r, c) in cardinals]

    def corroborate(self):
        total_removed = 0
        removed = None
        while removed != 0:
            removed = 0
            for r in range(self.rows):
                for c in range(self.columns):
                    neighbors = self.neighbors(r, c)
                    culled = self.cell_at(r, c).corroborate(neighbors)
                    removed += culled
            total_removed += removed
        return total_removed

    def guess(self):
        total_removed = 0
        tolerance = 0.0
        while tolerance < 0.5:
            _ = raw_input("Tolerance: %0.3f" % tolerance)
            removed = 0
            for row in self.cells:
                for cell in row:
                    removed += cell.guess(tolerance)
                    removed += self.corroborate()
            total_removed += removed
            tolerance += 0.01
        return total_removed
