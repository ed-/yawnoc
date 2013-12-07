#!/usr/bin/env python

from common.bashcolors import GRAYize
from common.bashcolors import RGBize
from conway.conway import Conway
from yawnoc.yawnoc import GardenOfEden
from yawnoc.yawnoc import Yawnoc
from random import seed
from random import random


class ColorConway(Conway):
    ALIVE = RGBize('[]', (5, 5, 5))
    DEAD = '  '


class ColorYawnoc(Yawnoc):
    def __str__(self):
        return '\n'.join((''.join(GRAYize('  ', cell.confidence)
                          for cell in row))
                         for row in self.cells)


def do_reversal(parser):
    parser.add_argument('filename', help="Load GOL file.")
    args = parser.parse_args()

    CC = Conway
    YC = Yawnoc
    if args.color:
        CC = ColorConway
        YC = ColorYawnoc

    C = CC.load(args.filename, ALIVE='[]', DEAD='  ')
    Y = YC(C)
    try:
        Y.corroborate(debug=args.debug)
        Y.guess(debug=args.debug)
        G = CC(Y.bestguess)
        print G
        print "Accuracy: %0.2f%%" % (100.0 * C.diff(G))
    except GardenOfEden:
        print "Looks like a Garden of Eden state."


def do_random_test(parser):
    parser.add_argument('rows', help="Height of field.", type=int)
    parser.add_argument('columns', help="Width of field.", type=int)
    parser.add_argument('-s', '--seed', help='Random seed.')
    parser.add_argument('-x', '--chance', type=float, help='Fill chance.')
    args = parser.parse_args()

    chance = 0.5 if args.chance is None else args.chance
    if args.seed is not None:
        seed(args.seed)
    cells = [[random() <= chance
              for c in range(args.columns)]
             for r in range(args.rows)]

    CC = Conway
    YC = Yawnoc
    if args.color:
        CC = ColorConway
        YC = ColorYawnoc

    C = CC(cells)

    print "Seed:"
    print C
    print

    C.step()
    print "Goal:"
    print C
    print

    Y = YC(C)

    Y.corroborate(debug=args.debug)
    print "Corroborated:"
    print Y
    print

    print "Spans:"
    print Y.spanstr
    print

    print "Confidence:"
    print Y.confstr
    print

    Y.guess(debug=args.debug)
    G = CC(Y.bestguess)
    print "Guess:"
    print G
    print

    print "Next:"
    G.step()
    print G
    print

    print "Accuracy: %0.2f%%" % (100.0 * C.diff(G))


if __name__ == '__main__':
    from argparse import ArgumentParser
    ap = ArgumentParser()

    COMMANDS = {
        'random': do_random_test,
        'reverse': do_reversal,
        }

    ap.add_argument('command', choices=COMMANDS.keys(),
                    help='Yawnoc command to run.')
    ap.add_argument('--color', action='store_true',
                    help="Use colorized output.")
    ap.add_argument('--debug', action='store_true',
                    help="Show progress during calculations.")

    args, _ = ap.parse_known_args()

    command = args.command
    if command in COMMANDS:
        COMMANDS[command](ap)
