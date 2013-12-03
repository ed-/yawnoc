from yawnoc import Yawnoc
from common.bashcolors import GRAYize


class ColorYawnoc(Yawnoc):
    def __str__(self):
        return '\n'.join((''.join(GRAYize('  ', cell.confidence)
                          for cell in row))
                         for row in self.cells)

    @property
    def confstr(self):
        return '\n'.join((' '.join('%0.3f' % cell.confidence
                          for cell in row))
                         for row in self.cells)

    @property
    def spanstr(self):
        return '\n'.join((' '.join('%3i' % len(cell.histories)
                          for cell in row))
                         for row in self.cells)

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
                    print self
                    print
            total_removed += removed
        return total_removed
