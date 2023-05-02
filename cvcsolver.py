import cvc5
from cvc5 import Kind

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
x = slv.mkConst(String, "x")

start = slv.mkConst(Int, "start")
length = slv.mkConst(Int, "length")
m = slv.mkConst(Int, "m")
k1 = slv.mkConst(Int, "k1")


ss = SplitSelect(slv)
slv.assertFormula(alpha.eqTerm(slv.mkTerm(Kind.APPLY_UF, ss, x, sep1, k1)))
slv.assertFormula(slv.mkTerm(Kind.STRING_CONTAINS, x, sep1))
slv.assertFormula(slv.mkTerm(Kind.STRING_LENGTH, sep1).eqTerm(slv.mkInteger(1)))
slv.assertFormula(beta.eqTerm(slv.mkTerm(Kind.APPLY_UF, ss, alpha, sep2, m)))
slv.assertFormula(slv.mkTerm(Kind.STRING_CONTAINS, alpha, sep2))
slv.assertFormula(slv.mkTerm(Kind.STRING_LENGTH, sep2).eqTerm(slv.mkInteger(1)))
slv.assertFormula(gamma.eqTerm(slv.mkTerm(Kind.STRING_SUBSTR, beta, start, length)))

slv.assertFormula(x.eqTerm(slv.mkString("Obama, Barack(1961-)")))
slv.assertFormula(gamma.eqTerm(slv.mkString("Obama")))
res = slv.checkSat()
while res.isSat():
    sep1v =  slv.getValue(sep1)
    sep2v = slv.getValue(sep2)
    k1v = slv.getValue(k1)
    mv = slv.getValue(m)
    startv = slv.getValue(start)
    lengthv = slv.getValue(length)
    print(sep1v, k1v, sep2v, mv, startv, lengthv)
    slv.assertFormula(sep1.eqTerm(sep1v).notTerm())
    res = slv.checkSat()

