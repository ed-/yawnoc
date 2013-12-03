from bash.colors import RGBize
from conway import Conway

class ColorConway(Conway):
    def __str__(self):
        gray = lambda c: (5, 5, 5) if c else (0, 0, 0)
        return '\n'.join((''.join(RGBize('  ', gray(cell))
                          for cell in row))
                         for row in self.cells)
