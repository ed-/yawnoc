#!/usr/bin/env python
# Load a GOL file, and analyze it to see what state came before.

from common.bashcolors import GRAYize
from common.bashcolors import RGBize
from conway.conway import Conway
from yawnoc.yawnoc import GardenOfEden
from yawnoc.yawnoc import Yawnoc


class ColorConway(Conway):
    ALIVE = RGBize('[]', (5, 5, 5))
    DEAD = '  '


class ColorYawnoc(Yawnoc):
    def __str__(self):
        return '\n'.join((''.join(GRAYize('  ', cell.confidence)
                          for cell in row))
                         for row in self.cells)

def find_garden(args):
    C = ColorConway.load(args.filename, ALIVE='[]', DEAD='  ')
    saved = ColorConway(C.cells)
    print "Given:"
    print C
    print

    Y = ColorYawnoc(C)
    try:
        Y.corroborate(debug=args.debug)
    except GardenOfEden:
        print "Looks like a GoE."
    else:
        print "Looks fine to me."
        print Y
        print

        print "Spans:"
        print Y.spanstr
        print

        print "Confidence:"
        print Y.confstr
        print


def main(args):
    C = ColorConway.load(args.filename, ALIVE='[]', DEAD='  ')
    saved = ColorConway(C.cells)
    print "Target:"
    print C
    print

    C.step()
    print "Given:"
    print C
    print

    Y = ColorYawnoc(C)
    Y.corroborate(debug=args.debug)
    print "Corroborated:"
    print Y
    print

    Y.guess(debug=args.debug)
    G = ColorConway(Y.bestguess)
    print "Guess:"
    print G
    print

    print "Next:"
    G.step()
    print G
    print

    print "Check:"
    print C
    print

    print "Score:"
    print C.diff(G)
    print

    #print "Spans:"
    #print Y.spanstr
    #print

    #print "Confidence:"
    #print Y.confstr
    #print

if __name__ == '__main__':
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-f', '--filename', help="Load GOL file.",
                    default='data/glider.gol')
    ap.add_argument('-D', '--debug', action='store_true',
                    help="Show progress during calculations.")
    args = ap.parse_args()
    main(args)
    #find_garden(args)
