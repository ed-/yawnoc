#!/usr/bin/env python
# Yawnoc tries to work Conway backwards.
from alibi import Alibi
from exceptions import BadGuess
from exceptions import GardenOfEden
from exceptions import Impossible


class Yawnoc(object):
    def __init__(self, conway):
        self.cells = [[Alibi(Z=cell)
                       for cell in row]
                      for row in conway.cells]
        for row in range(self.rows):
            edge = self.columns - 1
            self.cell_at(row, 0).filter(nw=False, w=False, sw=False)
            self.cell_at(row, edge).filter(ne=False, e=False, se=False)

        for column in range(self.columns):
            edge = self.rows - 1
            self.cell_at(0, column).filter(nw=False, n=False, ne=False)
            self.cell_at(edge, column).filter(sw=False, s=False, se=False)

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
            assert (row >= 0) and (row < self.rows)
            assert (column >= 0) and (column < self.columns)
            return self.cells[row][column]
        except (AssertionError, IndexError):
            return None

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
                culled = self.cell_at(r, c).guess(0.5)
                if culled:
                    try:
                        self.corroborate(debug=debug)
                    except GardenOfEden:
                        # Let's assume it was a bad guess.
                        raise BadGuess()
                if debug and culled:
                    print self
                    print
