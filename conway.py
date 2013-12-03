class Conway(object):
    cells = None

    def __init__(self, cells):
        self.cells = cells[:]

    def __str__(self):
        T = {True: '#', False: '.'}
        return '\n'.join(' '.join(T[cell] for cell in row)
                         for row in self.cells)

    @property
    def rows(self):
        return len(self.cells)

    @property
    def columns(self):
        if not self.cells:
            return 0
        return len(self.cells[0])

    def _cell_at(self, row, column):
        try:
            assert row >= 0
            assert column >= 0
            return self.cells[row][column]
        except (AssertionError, IndexError):
            return False

    def neighborhood(self, row, column):
        return  [self._cell_at(row + r, column + c)
                 for r in (-1, 0, 1)
                 for c in (-1, 0, 1)]

    def _gol(self, row, column):
        neighborhood = self.neighborhood(row, column)
        center = neighborhood.pop(4)
        neighbors = sum([1 if cell else 0 for cell in neighborhood])
        return (center, neighbors) in [(True, 2), (True, 3), (False, 3)]

    def step(self):
        self.cells = [[self._gol(r, c)
                       for c in range(self.columns)]
                      for r in range(self.rows)]
