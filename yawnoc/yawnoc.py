#!/usr/bin/env python
# Yawnoc tries to work Conway backwards.
from alibi import Alibi
from exceptions import BadGuess
from exceptions import GardenOfEden
from exceptions import Impossible


def neighborhood(r, c):
    return [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
            (r, c - 1), (r, c + 1),
            (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]


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
        return [self.cell_at(r, c) for (r, c) in neighborhood(row, column)]

    def corroborate(self, check=None, debug=False):
        total_removed = 0
        rc = check
        if rc is None:
            rc = [(r, c) for r in range(self.rows)
                  for c in range(self.columns)]
        tolerance = lambda x: abs(0.5 - self.cell_at(*x).confidence)
        ftolerance = lambda x: -1 if self.cell_at(*x) is None else tolerance(x)
        while rc:
            removed = 0
            rc = sorted(list(set(rc)), key=ftolerance, reverse=True)
            r, c = rc.pop()
            if self.cell_at(r, c) is None:
                continue
            neighbors = self.neighbors(r, c)
            try:
                culled = self.cell_at(r, c).corroborate(neighbors)
                removed += culled
                if culled:
                    rc.extend(neighborhood(r, c))
                    if debug:
                        print self, len(rc)
                        print
            except Impossible:
                raise GardenOfEden()
            total_removed += removed
        return total_removed

    def guess(self, debug=False):
        total_removed = 0
        rc = [(r, c) for r in range(self.rows)
              for c in range(self.columns)]
        tolerance = lambda x: abs(0.5 - self.cell_at(*x).confidence)
        ftolerance = lambda x: -1 if self.cell_at(*x) is None else tolerance(x)
        while rc:
            removed = 0
            rc = sorted(list(set(rc)), key=ftolerance)
            r, c = rc.pop()
            if self.cell_at(r, c) is None:
                continue
            culled = self.cell_at(r, c).guess(0.5)
            if culled:
                try:
                    self.corroborate(check=[(r, c)], debug=debug)
                except GardenOfEden:
                    # Let's assume it was a bad guess.
                    raise BadGuess()
