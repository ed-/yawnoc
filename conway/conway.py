class Conway(object):
    cells = None
    ALIVE = '[]'
    DEAD = '  '

    def __init__(self, cells):
        self.cells = cells[:]

    def __str__(self):
        T = {True: self.ALIVE, False: self.DEAD}
        return '\n'.join(''.join(T[cell] for cell in row)
                         for row in self.cells)

    @classmethod
    def load(cls, filename, ALIVE=None, DEAD=None):
        ALIVE = ALIVE or cls.ALIVE
        DEAD = DEAD or cls.DEAD
        with open(filename, 'r') as inf:
            filedata = [line for line in inf.read().split('\n') if line]
            data = []
            for line in filedata:
                linedata = []
                while line:
                    if line.startswith(ALIVE):
                        linedata.append(True)
                        line = line[len(ALIVE):]
                    elif line.startswith(DEAD):
                        linedata.append(False)
                        line = line[len(DEAD):]
                    else:
                        print "wh"
                        line = line[1:]
                data.append(linedata)
            return cls(data)

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
        return [self._cell_at(row + r, column + c)
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
