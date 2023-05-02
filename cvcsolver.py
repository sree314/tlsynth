import cvc5
from cvc5 import Kind
from solver import SplitSplitSubstrXYSln
from ops import Case, SplitSplitSubstr

def SplitSelect(slv):
    String = slv.getStringSort()

    s = slv.mkVar(String, "s")
    sep = slv.mkVar(String, "sep")
    k = slv.mkVar(slv.getIntegerSort(), "k")

    zero = slv.mkInteger(0)

    p = slv.mkTerm(Kind.STRING_INDEXOF, s, sep, zero)

    a1 = slv.mkTerm(Kind.STRING_SUBSTR, s, zero, p)
    a2 = slv.mkTerm(Kind.STRING_SUBSTR, s,
                    slv.mkTerm(Kind.ADD, p, slv.mkInteger(1)),
                    slv.mkTerm(Kind.STRING_LENGTH, s))

    body = slv.defineFun("SplitSelect", [s, sep, k], String,
                         k.eqTerm(zero).iteTerm(a1, a2),
                         True)
    return body

def Substr(slv):
    String = slv.getStringSort()

    s = slv.mkVar(String, "s")
    start = slv.mkVar(slv.getIntegerSort(), "start")
    length = slv.mkVar(slv.getIntegerSort(), "length")

    minusone = slv.mkInteger(-1)

    body = minusone.eqTerm(length).iteTerm(
        slv.mkTerm(Kind.STRING_SUBSTR, s, start, slv.mkTerm(Kind.STRING_LENGTH, s)),
        slv.mkTerm(Kind.STRING_SUBSTR, s, start, length))

    return slv.defineFun("Substr", [s, start, length], String,
                         body,
                         True)

def SolveSplitSplitSubstrXY(x, y):
    slv = cvc5.Solver()
    slv.setLogic("QF_SLIA")
    slv.setOption("produce-models", "true")
    slv.setOption("strings-exp", "true")
    slv.setOption("output-language", "smt2")
    slv.setOption("strings-fmf", "true")

    String = slv.getStringSort()
    Int = slv.getIntegerSort()

    alpha = slv.mkConst(String, "alpha")
    beta = slv.mkConst(String, "beta")
    gamma = slv.mkConst(String, "gamma")
    sep1 = slv.mkConst(String, "sep1")
    sep2 = slv.mkConst(String, "sep2")
    xvar = slv.mkString(x)

    start = slv.mkConst(Int, "start")
    length = slv.mkConst(Int, "length")
    m = slv.mkConst(Int, "m")
    k1 = slv.mkConst(Int, "k1")

    ss = SplitSelect(slv)
    mySubstr = Substr(slv)

    slv.assertFormula(alpha.eqTerm(slv.mkTerm(Kind.APPLY_UF, ss, xvar, sep1, k1)))
    slv.assertFormula(slv.mkTerm(Kind.STRING_CONTAINS, xvar, sep1))
    slv.assertFormula(slv.mkTerm(Kind.STRING_LENGTH, sep1).eqTerm(slv.mkInteger(1)))
    slv.assertFormula(beta.eqTerm(slv.mkTerm(Kind.APPLY_UF, ss, alpha, sep2, m)))
    slv.assertFormula(slv.mkTerm(Kind.STRING_CONTAINS, alpha, sep2))
    slv.assertFormula(slv.mkTerm(Kind.STRING_LENGTH, sep2).eqTerm(slv.mkInteger(1)))
    slv.assertFormula(gamma.eqTerm(slv.mkTerm(Kind.APPLY_UF, mySubstr, beta, start, length)))
    slv.assertFormula(gamma.eqTerm(slv.mkString(y)))

    case = []
    if y in x:
        case.append(Case.UNCHANGED)
    else:
        if y.isupper() and y in x.upper():
            case.append(Case.UPPER)

        if y.islower() and y in x.lower():
            case.append(Case.LOWER)

    res = slv.checkSat()
    while res.isSat():
        sep1v =  slv.getValue(sep1)
        sep2v = slv.getValue(sep2)
        k1v = slv.getValue(k1)
        mv = slv.getValue(m)
        startv = slv.getValue(start)
        lengthv = slv.getValue(length)

        for c in case:
            yield SplitSplitSubstrXYSln(sep1v.getStringValue(),
                                        k1v.getIntegerValue(),
                                        sep2v.getStringValue(),
                                        mv.getIntegerValue(),
                                        startv.getIntegerValue(),
                                        lengthv.getIntegerValue(), c)

        #TODO: this doesn't necessarily generate all the terms
        slv.assertFormula(sep1.eqTerm(sep1v).notTerm())
        res = slv.checkSat()

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


if __name__ == "__main__":
    test_SolveSplitSplitSubstrXY()

