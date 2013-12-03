#!/usr/bin/env python

from conway.colorconway import ColorConway as Conway
from yawnoc.coloryawnoc import ColorYawnoc as Yawnoc

def main(data):
    C = Conway(data)
    print "Target:"
    print C
    print

    C.step()
    print "Given:"
    print C
    print

    Y = Yawnoc(C)
    print "Yawnoc:"
    print Y
    print

    Y.corroborate()
    print "Corroborated:"
    print Y
    print

    print "Clue:"
    print C
    print

    #Y.guess()
    #print "Guess:"
    #print Y
    #print

    #guessdata = [[c > 0.5 for c in row] for row in Y.confidence]
    #G = Conway(guessdata)
    #print "Guess:"
    #print G
    #print 

    #G.step()
    #print "Next:"
    #print G
    #print

    #print "Compare:"
    #print C
    #print


if __name__ == '__main__':
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-f', '--filename', help="Load GOL file.",
                    default='data/glider.gol')
    args = ap.parse_args()
    with open(args.filename, 'r') as inf:
        T = (line.strip() for line in inf.readlines()
             if line.strip() != '')
        T = (line.split(' ') for line in T)
        T = [[c in "1X#" for c in row] for row in T]
        main(T)
