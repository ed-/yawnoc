from cell import Cell
# Conway's Game of Life
ALIVE = '#'
DEAD = '.'
DONTCARE = '?'

class Conway(object):
    width = 0
    height = 0
    cells = None

    def __init__(self, width, height, cells=None):
        self.width = width
        self.height = height
        if cells:
            self.cells = cells
        else:
            self.cells = [[Cell(False)
                           for c in range(width)]
                          for r in range(height)]

    def __str__(self):
        return self.dumps()

    def dumps(self, alive=ALIVE, dead=DEAD, dontcare=DONTCARE):
        lookup = {True: alive, False: dead, None: dontcare} 
        return '\n'.join([' '.join([lookup[self.cell_at(row, column)]
                                    for column in range(self.width)]) 
                          for row in range(self.height)])

    def dump(self, filename, alive=ALIVE, dead=DEAD, dontcare=DONTCARE):
        with open(filename, 'w') as outf:
            outf.write(self.dumps(alive, dead, dontcare))

    @classmethod
    def loads(cls, string, alive=ALIVE, dead=DEAD, dontcare=DONTCARE):
        lookup = {alive: True, dead: False, dontcare: None}
        Z = []
        for line in string.split('\n'):
            if not line:
                continue
            row = line.strip().split()
            row = [Cell(lookup[cell]) for cell in row]
            Z.append(row)
        width = max(len(row) for row in Z)
        height = len(Z)
        return cls(width, height, Z)

    @classmethod
    def load(cls, filename, alive=ALIVE, dead=DEAD, dontcare=DONTCARE):
        with open(filename, 'r') as inf:
            return cls.loads(inf.read())

    def cell_at(self, row, column):
        if row < 0 or column < 0:
            return None
        if row >= self.height or column >= self.width:
            return None
        if not self.cells[row] or not self.cells[row][column]:
            return None
        return self.cells[row][column].state

    def tick(self):
        for r, row in enumerate(self.cells):
            for c, cell in enumerate(row):
                current = self.cell_at(r, c)
                if current is None:
                    continue
                neighbors = [(r + i, c + j)
                             for i in (-1, 0, 1)
                             for j in (-1, 0, 1)]
                neighbors = [rc for rc in neighbors if rc != (r, c)]
                neighbors = [self.cell_at(nr, nc) for (nr, nc) in neighbors]
                living = len([n for n in neighbors if n])
                if current is None:
                    continue
                if current:
                    cell.prep(True if living in (2, 3) else False)
                else:
                    cell.prep(True if living == 3 else False)
        for row in self.cells:
            for cell in row:
                cell.tick()
