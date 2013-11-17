#!/usr/bin/env python
# Yawnoc tries to work Conway backwards.
from conway import ALIVE, DEAD, DONTCARE
from historycloud import HistoryCloud
from copy import deepcopy

class Yawnoc(object):
    width = 0
    height = 0
    hcs = None

    def __init__(self, width, height, cells=None):
        self.width = width
        self.height = height
        if cells:
            self.cells = cells
        else:
            self.cells = [[HistoryCloud()
                           for c in range(width)]
                          for r in range(height)]
        for c in range(width):
            for r in range(height):
                self.cells[r][c].ROW = r
                self.cells[r][c].COL = c

    def __str__(self):
        result = []
        for sp, co in zip(self.spans.split('\n'), self.confidence.split('\n')):
            result.append(sp + '\t\t' + co)
        return '\n'.join(result)

    def __repr__(self):
        return str(self)

    @property
    def spans(self):
        return '\n'.join([' '.join(['%3d' % len(self.cell_at(row, column))
                                    for column in range(self.width)])
                          for row in range(self.height)])

    @property
    def confidence(self):
        return '\n'.join([' '.join(['%0.3f' % self.cell_at(row, column).confidence
                                    for column in range(self.width)])
                          for row in range(self.height)])

    @classmethod
    def loads(cls, string, alive=ALIVE, dead=DEAD, dontcare=DONTCARE):
        lookup = {alive: True, dead: False, dontcare: None}
        Z = []
        for line in string.split('\n'):
            if not line:
                continue
            row = line.strip().split()
            row = [HistoryCloud(Z=lookup[cell]) for cell in row]
            Z.append(row)
        width = max(len(row) for row in Z)
        height = len(Z)
        return cls(width, height, Z)

    @classmethod
    def load(cls, filename, alive=ALIVE, dead=DEAD, dontcare=DONTCARE):
        with open(filename, 'r') as inf:
            return cls.loads(inf.read())

    def cell_at(self, row, column):
        #dummy = HistoryCloud(Z=0)
        dummy = HistoryCloud()
        use_dummy = False
        if row < 0:
            dummy.filter(nw=0, n=0, ne=0)
            use_dummy = True
        if column < 0:
            dummy.filter(nw=0, w=0, sw=0)
            use_dummy = True
        if row >= self.height:
            dummy.filter(sw=0, s=0, se=0)
            use_dummy = True
        if column >= self.width:
            dummy.filter(ne=0, e=0, se=0)
            use_dummy = True
        if use_dummy:
            return dummy
        if not self.cells[row] or not self.cells[row][column]:
            return HistoryCloud()
        return self.cells[row][column]

    def corroborate(self):
        removed = -1
        total = 0
        while removed != 0:
            removed = 0
            for r in range(self.height):
                for c in range(self.width):
                    neighbors = [(r + i, c + j)
                                 for i in (-1, 0, 1)
                                 for j in (-1, 0, 1)]
                    neighbors = [rc for rc in neighbors if rc != (r, c)]
                    neighbors = [self.cell_at(nr, nc)
                        for (nr, nc) in neighbors]
                    current = self.cell_at(r, c)
                    culled = current.corroborate(neighbors)
                    if culled:
                        self.cells[r][c].hs = current.hs[:]
                    removed += culled
            total += removed
        return total

    def guess(self, r, c, was):
        self.cells[r][c].filter(c=was)
        self.corroborate()


if __name__ == '__main__':
    y = Yawnoc.load('spinner.txt')
    print y
    print
    y.corroborate()
    print y
