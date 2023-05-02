#!/usr/bin/env python3

import itertools
import csv
from ops import *
from optree import *

def EnumerateBestLogicalOp(Inp, Out, cols):
    # SplitSplitSubstr(x, 0, "(", 0, " ", 1, 0, -1, None)

    #cols = list([i for i in range(len(Inp[0])) if isinstance(Inp[0][i], str)])
    seps = None
    MAX_SEP_LENGTH = 1

    for row in Inp:
        cur_seps = []
        for seplength in range(1, MAX_SEP_LENGTH+1):
            # TODO: support extracting separators from columns other than the first
            cur_seps.extend(ngrams(row[cols[0]], seplength))

        if seps is None:
            seps = set(cur_seps)
        else:
            # this is useful to shrink the number of separators even more
            seps = seps.intersection(set(cur_seps))

    t = set(Out)
    if len(t) == 1:
        yield Op(Constant, t.pop())

    seps = set(seps)
    split_indexes = [0, 1]
    max_length = max([len(s) for s in [row[0] for row in Inp]])
    possible_starts = list(range(max_length))
    possible_lengths = [-1] + possible_starts
    cases = [Case.UNCHANGED, Case.UPPER, Case.LOWER]

    for k, start, length, case in itertools.product(cols, possible_starts, possible_lengths, cases):
        yield Op(Substr, k, start, length, case)

    for k, sep, m, start, length, case in itertools.product(cols, seps, split_indexes, possible_starts, possible_lengths, cases):
        yield Op(SplitSubstr, k, sep, m, start, length, case)

    for k1, sep1, k2, sep2, m, start, length, case in itertools.product(cols, seps, split_indexes, seps, split_indexes, possible_starts, possible_lengths, cases):
        yield Op(SplitSplitSubstr, k1, sep1, k2, sep2, m, start, length, case)

def progress(partial_output, Out):
    p_s = 0
    p_e = 0
    for po, o in zip(partial_output, Out):
        if o.startswith(po):
            p_s += len(po)

        if o.endswith(po):
            p_e += len(po)

    return max(p_s, p_e)

def TryLearnTransform2(Inp, Out, cols, EnumerateBestLogicalOp):
    print("TTL2")
    print("Inp", cols, Inp)
    print("Out", Out)
    #while True: # not needed due to EnumerateBestOpLoop
    max_progress = 0
    max_progress_op = None
    max_P = None

    for xop in EnumerateBestLogicalOp(Inp, Out, cols):
        lop = xop.get_lambda()
        P = [lop(i).execute() for i in Inp] # also might collect stats on progress?
        current_progress = progress(P, Out)
        if current_progress > max_progress:
            max_progress = current_progress
            max_progress_op = xop
            max_P = P
            print("***", current_progress, P, xop)

    if max_progress_op is None:
        return None

    P = max_P
    print("P", P)
    Oleft, is_empty = LeftRemainder(Out, P)
    print("left", Oleft)
    if is_empty:
       left_op = None
    else:
       left_op = TryLearnTransform2(Inp, Oleft, cols, EnumerateBestLogicalOp)
       if left_op is None:
           return None

    Oright, is_empty = RightRemainder(Out, P)
    print("right", Oright)

    if is_empty:
       right_op = None
    else:
        right_op = TryLearnTransform2(Inp, Oright, cols, EnumerateBestLogicalOp)
        if right_op is None:
            return None

    return OpTree(max_progress_op.get_lambda(), left_op, right_op, max_progress_op)

def load_csv(fn, header = True):
    with open(fn, "r") as f:
        data = csv.reader(f)
        read_header = False
        out = []
        for row in data:
            if header and not read_header:
                read_header = True
                continue

            out.append(row)

        return out

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
