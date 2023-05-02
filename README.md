# Exercises in Program Synthesis

This code implements the transformation learning described in Section
3.2 of the paper by Zhu, He, and Chaudhuri, "[Auto-Join: Joining Tables
by Leveraging Transformations](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/autojoin-fullversion.pdf)" that appears in the Proceedings of the VLDB Endowment.

I make no claims of completeness of this implementation, it was
basically a small enough problem to demonstrate various approaches to
program synthesis on a real problem.  It is unclear what approach the
original authors used since they did not release their source code.

I acknowledge my colleague, Fatemeh Nargesian, who pointed the paper
out to me.

This repository contains three approaches to solve the underlying
program synthesis problem.

  - `tl.py`, uses a brute-force CSP-style approach.
  - `tlsolv.py` (and the code in `solver.py`) which implements a "deductive" program synthesis approach
  - `cvcsolver.py`, a prototype that uses a SMT solver ([cvc5](https://cvc5.github.io/)) to implement a solver, though it is slower than `tlsolv.py` and does not yet produce all possible solutions.


## Running

To run `tl.py` or `tlsolv.py`, run:

```
python3 ./tl.py tests/pres1.csv tests/pres2.csv
...
FUNCTION Concat(SplitSplitSubstr(ROW, 0, ' ', 1, '(', 0, 0, -1, Case.UNCHANGED), Concat(Constant(' '), SplitSubstr(ROW, 0, ',', 0, 0, -1, Case.UNCHANGED)))
...
```

For the other example, run:
```
python3 ./tlsolv.py tests/school1.csv tests/school2.csv --sc 1
```
