#!/usr/bin/env python

from conway import Conway
from random import seed
from random import random

def coin(chance=0.5):
    return random() <= chance

class RandomConway(Conway):
    cells = None

    def __init__(self, rows, columns, chance=0.5):
        self.cells = [[coin(chance)
                       for c in range(columns)]
                      for r in range(rows)]

if __name__ == '__main__':
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-r', '--rows', help="Height of field.",
                    required=True, type=int)
    ap.add_argument('-c', '--columns', help="Width of field.",
                    required=True, type=int)
    ap.add_argument('-s', '--seed', help='Random seed.')
    ap.add_argument('-x', '--chance', type=float, help='Fill chance.')
    args = ap.parse_args()
    if args.seed is not None:
        seed(args.seed)
    chance = 0.5 if args.chance is None else args.chance
    print RandomConway(args.rows, args.columns, chance)

