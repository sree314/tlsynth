#!/usr/bin/env python3

import itertools
import csv
from ops import *
from solver import *
from optree import *
from tl import TryLearnTransform2, load_csv

def EnumerateBestLogicalOp(Inp, Out, cols):
    out = Out[0]
    prefixes = [out[:i] for i in reversed(range(1, len(out)+1))]
    suffixes = [out[-i:] for i in reversed(range(len(out)+1))]

    for p, s in zip(prefixes, suffixes):
        for sol in itertools.chain(SolveConstant(Inp[0], p, cols), SolveConstant(Inp[0], s, cols)):
            yield Op(Constant, sol.v)

        for sol in itertools.chain(SolveSubstr(Inp[0], p, cols),
                                   SolveSubstr(Inp[0], s, cols)):
            yield Op(Substr, sol.k, sol.start, sol.length, sol.c)

        for sol in itertools.chain(SolveSplitSubstr(Inp[0], p, cols),
                                   SolveSplitSubstr(Inp[0], s, cols)):
            yield Op(SplitSubstr, sol.k, sol.sep, sol.m, sol.start, sol.length, sol.c)

        for sol in itertools.chain(SolveSplitSplitSubstr(Inp[0], p, cols),
                                  SolveSplitSplitSubstr(Inp[0], s, cols)):
           yield Op(SplitSplitSubstr, sol.k1, sol.sep1, sol.k2, sol.sep2, sol.m,
                    sol.start, sol.length, sol.c)



if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Learn function for joining two columns")

    p.add_argument("srccsv", help="Source CSV")
    p.add_argument("tgtcsv", help="Target CSV")
    p.add_argument("--sc", dest="src_column", help="Source column", default=0, type=int)
    p.add_argument("--tc", dest="tgt_column", help="Target column", default=0, type=int)

    args = p.parse_args()

    source = load_csv(args.srccsv)
    target = load_csv(args.tgtcsv)
    tgtcol = [s[args.tgt_column] for s in target]

    o = TryLearnTransform2(source, tgtcol, [args.src_column], EnumerateBestLogicalOp)
    if o is not None:
        print("FUNCTION", o)
        for tt,exp in zip(source, tgtcol):
            print(o.execute(tt), "|", exp)
    else:
        print("No function found")
