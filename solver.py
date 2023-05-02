#!/usr/bin/env python3

import itertools
from collections import namedtuple
from ops import Substring, SelectK, SplitSubstr, Split, SplitSplitSubstr, Case

SubstringSln = namedtuple('SubstringSln', 'start length c')
SelectKSln = namedtuple('SelectKSln', 'k')
SubstrSln = namedtuple('SubstrSln', 'k start length c')
SplitSln = namedtuple('SplitSln', 'sep')
SplitSelectKSln = namedtuple('SplitSelectKSln', 'sep k')
ConstantXYSln = namedtuple('ConstantXYSln', 'v')
ConstantSln = namedtuple('ConstantSln', 'k v')

SS = namedtuple('SplitSubstrSolution', 'k sep m start length')

def SolveSubstring(x, y, offset = 0, end = None):
    # substr(x, start, length, c) = y => x = Ay'B and len(A) = start and ((len(B) > 0 and length != -1) or (len(B) == 0 and length == -1)
    # where case_change(y') = y

    pc = []

    tocheck = [(x, Case.UNCHANGED)]

    if y.islower():
        tocheck = [(x.lower(), Case.LOWER)]

    if y.isupper():
        tocheck = [(x.upper(), Case.UPPER)]

    for xx, c in tocheck:
        p = xx.find(y)
        while p != -1:
            pc.append((p, c))
            p = xx.find(y, p + 1)

    send = end if end is not None else len(x)
    for p, c in pc:
        if p + len(y) == send:
            yield SubstringSln(start = p - offset, length = -1, c = c)

        yield SubstringSln(start = p - offset, length = len(y), c = c)

def test_SolveSubstring():
    tt = [('caterpillar', 'CAT', 1),
          ('dachshund', 'hund', 2),
          ('pergola', 'c', 0),]

    for x, y, slns in tt:
        count = 0
        for s in SolveSubstring(x, y):
            print(s)
            yy = Substring(x, s.start, s.length, s.c).execute()
            assert yy == y, f"{yy} != {y}"
            count += 1

        assert count == slns

def SolveSelectK(xarr, y):
    # selectk(arr, k) = y => arr[k] = y

    for k, x in enumerate(xarr):
        if x == y:
            yield SelectKSln(k = k)

def test_SelectK():
    tt = [(['caterpillar', 'cat'], 'cat', 1),
          (['dachshund', 'hund'], 'hund', 1),
          (['pergola', 'water'], 'melon', 0)]

    for xarr, y, slns in tt:
        count = 0
        for s in SolveSelectK(xarr, y):
            yy = SelectK(xarr, s.k).execute()
            assert yy == y, f"{yy} != {y}"
            count += 1

        assert count == slns

def SolveSplit(x, yarr):
    # split(x, sep) = yarr => sep = x[len(yarr[0])] if len(yarr[0]) != x
    if len(yarr[0]) != len(x):
        sep = x[len(yarr[0])]
        if x.find(sep) == len(yarr[0]):
            yield SplitSln(sep = sep)

def test_SolveSplit():
    tt = [('cater@pillar', ['cater', 'pillar'], 1)]

    for x, y, slns in tt:
        count = 0
        for s in SolveSplit(x, y):
            yy = Split(x, s.sep).execute()
            assert yy == y, f"{yy} != {y}"
            count += 1

        assert count == slns

def SolveSplitSelectK(x, y):
    # SelectK(Split(x, sep), k) = y =>
    # if k == 0: x = y sep B
    # if k == 1: x = A sep y

    if len(x) <= len(y):
        return

    if x.startswith(y):
        for s in SolveSplit(x, [y, x[len(y)+2:]]):
            yield SplitSelectKSln(sep = s.sep, k = 0)

    if x.endswith(y):
        for s in SolveSplit(x, [x[:-(len(y)+1)], y]):
            yield SplitSelectKSln(sep = s.sep, k = 1)

def test_SolveSplitSelectK():
    tt = [('cater@pillar', 'pillar', 1),
          ('cater@pillar', 'cater', 1),
          ('cater@pillar', 'x', 0),
    ]

    for x, y, slns in tt:
        count = 0
        for s in SolveSplitSelectK(x, y):
            yy = SelectK(Split(x, s.sep).execute(), s.k).execute()
            assert yy == y, f"{yy} != {y}"
            count += 1

        assert count == slns

def SolveConstantXY(x, y):
    # Constant(x) = y => x == y

    if x == y:
        yield ConstantXYSln(v = x)

def SolveConstant(inp, out, cols):
    # TODO:
    for kndx in cols:
        yield ConstantSln(k = kndx, v = out)

def SolveSubstr(inp, out, cols, offset = 0, end = None):
    k = list([kk for kk in cols if out.lower() in inp[kk].lower()])
    kinps = [inp[kk] for kk in k]

    sols = []
    for X, kndx in zip(kinps, k):
        for sol in SolveSubstring(X, out, offset, end):
            sols.append(SubstrSln(k = kndx, start = sol.start, length = sol.length, c = sol.c))

    return sols

def test_SolveSubstr():
    inp = ['cat', 'caterpillar', 'strcat', 'help']
    out = 'cat'

    for x in SolveSubstr(inp, out, list(range(len(inp)))):
        print(x)

SplitSubstrXYSln = namedtuple('SplitSubstrXYSln', 'sep m start length c')

def get_supstrings(x, y):
    #TODO: add separators, maybe reorder affixes to maximize length?
    #TODO: handle case better

    ypos = x.lower().find(y.lower())
    ylen = len(y)
    while ypos != -1:
        yorig = x[ypos:ypos+ylen]

        prefix = list([x[ypos-i:ypos] for i in range(0, ypos+1)])
        suffix = list([x[ypos+len(y):j] for j in range(ypos+len(y), len(x)+1)])
        #print(prefix, suffix, ypos)
        for a, b in itertools.product(prefix, suffix):
            yield a + yorig + b

        ypos = x.lower().find(y.lower(), ypos + 1)

def SolveSplitSubstrXY(x, y):
    # SplitSubstrXY(x, sep, m, start, length, c) =
    #    Substring(SelectK(Split(x, sep), m), start, length, c)
    # alpha = SelectK(Split(x, sep), m)
    # beta = Substring(alpha, start, length, c)
    # y = beta
    #
    # alpha = A y B
    # x = alpha sep D and or x = D sep alpha

    for alpha in get_supstrings(x, y):
        #print(alpha)
        for s1 in SolveSubstring(alpha, y):
            for s2 in SolveSplitSelectK(x, alpha):
                yield SplitSubstrXYSln(sep = s2.sep, m = s2.k, start = s1.start,
                                       length = s1.length,
                                       c = s1.c)

def test_SolveSplitSubstrXY():
    tt = [('Proper Case', 'case'),]

    for x, y in tt:
        count = 0
        for s in SolveSplitSubstrXY(x, y):
            print(s)
            yy = SplitSubstr([x], 0, s.sep, s.m, s.start, s.length, s.c).execute()
            assert yy == y, f"{yy} != {y}"
            count += 1

        print(count, "Solutions")

SplitSplitSubstrXYSln = namedtuple('SplitSplitSubstrXYSln', 'sep1 k2 sep2 m start length c')
def SolveSplitSplitSubstrXY(x, y):
    # SplitSplitSubstrXY(x, sep1, k2, sep2, m, start, length, c) =
    #    Substring(SelectK(Split(SelectK(Split(x, sep1), k1), sep2), m), start, length, c)
    # alpha = SelectK(Split(x, sep1), k1)
    # beta = SelectK(Split(alpha, sep2), m)
    # gamma = Substring(beta, start, length, c)
    # y = gamma
    #
    # gamma = A beta B

    # x = alpha sep1 REST or REST sep1 alpha
    # alpha = beta sep2 REST1      or REST1 sep2 beta

    # [0, (0-n)] [(0-n), n]
    for alphastart, alphaend in itertools.chain(itertools.product([0], range(1, len(x))),
                                                itertools.product(range(0,len(x)), [len(x)])):
        alpha = x[alphastart:alphaend]

        for s3 in SolveSplitSelectK(x, alpha):
            for beta in get_supstrings(x, y):
                for s2 in SolveSplitSelectK(alpha, beta):
                    for s1 in SolveSubstring(beta, y):
                        yield SplitSplitSubstrXYSln(sep1 = s3.sep, k2 = s3.k,
                                                    sep2 = s2.sep, m = s2.k,
                                                    start = s1.start, length = s1.length,
                                                    c = s1.c)

def test_SolveSplitSplitSubstrXY():
    tt = [('Obama, Barack(1961-)', 'Obama')]
    for x, y in tt:
        count = 0
        for s in SolveSplitSplitSubstrXY(x, y):
            print(s)
            yy = SplitSplitSubstr([x], 0, s.sep1, s.k2, s.sep2, s.m, s.start, s.length, s.c).execute()
            assert yy == y, f"{yy} != {y}"
            count += 1

        print(count, "Solutions")

SplitSubstrSln = namedtuple('SplitSubstrSln', 'k sep m start length c')
def SolveSplitSubstr(inp, out, cols):
    k = list([kk for kk in cols if out.lower() in inp[kk].lower()])
    kinps = [inp[kk] for kk in k]

    for X, kndx in zip(kinps, k):
        for s in SolveSplitSubstrXY(X, out):
            yield SplitSubstrSln(k = kndx, sep = s.sep, m = s.m, start = s.start,
                                 length = s.length, c = s.c)

SplitSplitSubstrSln = namedtuple('SplitSplitSubstrSln', 'k1 sep1 k2 sep2 m start length c')
def SolveSplitSplitSubstr(inp, out, cols):
    k = list([kk for kk in cols if out.lower() in inp[kk].lower()])
    kinps = [inp[kk] for kk in k]

    for X, kndx in zip(kinps, k):
        for s in SolveSplitSplitSubstrXY(X, out):
            yield SplitSplitSubstrSln(k1 = kndx, sep1 = s.sep1, k2 = s.k2,
                                      sep2 = s.sep2, m = s.m,
                                      start = s.start, length = s.length, c = s.c)

# def SolveSplitSubstr2(inp, out, cols):
#     k = list([kk for kk in cols if out in inp[kk]])
#     kinps = [inp[kk] for kk in k]

#     sols = []
#     for X, kndx in zip(kinps, k):
#         p = X.find(out)
#         if p != -1:
#             possible_seps = dict()
#             for pos, c in enumerate(X):
#                 if c not in possible_seps:
#                     possible_seps[c] = pos

#             if p > 0:
#                 sep_before = max([ps for ps in possible_seps.items() if ps[1] < p], key=lambda ps: ps[1])
#             else:
#                 sep_before = None

#             if p + len(out) + 1 < len(X):
#                 sep_after = min([ps for ps in possible_seps.items() if ps[1] >= p + len(out)], key=lambda ps: ps[1])
#             else:
#                 sep_after = None

#             if sep_after:
#                 sep, sep_pos = sep_after
#                 if p + len(out) == sep_pos:
#                     sols.append(SS(k = kndx, sep = sep, m = 0, start = p, length = -1))

#                 sols.append(SS(k = kndx, sep = sep, m = 0, start = p, length = len(out)))

#             if sep_before:
#                 sep, sep_pos = sep_before
#                 if p + len(out) == len(X):
#                     sols.append(SS(k = kndx, sep = sep, m = 1, start = p - sep_pos, length = -1))

#                 sols.append(SS(k = kndx, sep = sep, m = 1, start = p - sep_pos, length = len(out)))

#     return sols

# def SolveX(Inp, Out, cols):
#     out = Out[0]
#     prefixes = [out[:i] for i in reversed(range(1, len(out)+1))]
#     suffixes = [out[-i:] for i in reversed(range(len(out)+1))]

#     for p, s in zip(prefixes, suffixes):
#         for sol in itertools.chain(SolveSplitSubstr(Inp[0], p, cols),
#                                    SolveSplitSubstr(Inp[0], s, cols)):
#             yy = SplitSubstr(Inp[0], sol.k, sol.sep, sol.m, sol.start, sol.length, sol.c).execute()
#             print(sol, '[' + yy + ']')

if __name__ == "__main__":
    cols = [0]

    Inp = [['Obama, Barack(1961-)', ' 47.0'],
           ['Bush, George W.(1946-)', ' 49'],
           ['Clinton, Bill(1946-)', ' 55'],
           ['Bush, George H. W.(1924-)', ' 60'],
           ['Reagan, Ronald(1911-2004)', ' 52']]

    Out = [' Obama', ' Bush', ' Clinton', ' Bush', ' Reagan']

    #SolveX(Inp, Out, cols)
    #test_SolveSubstring()
    #test_SelectK()
    #test_SolveSplit()
    #test_SolveSplitSelectK()
    test_SolveSplitSubstrXY()
    #test_SolveSubstr()
    #test_SolveSplitSplitSubstrXY()
