from ops import Constant

class OpTree:
    def __init__(self, op, left, right, xop):
        self.op = op
        self.left = left
        self.right = right
        self.xop = xop

    def __str__(self):
        v = [repr(x) for x in [self.left, self.xop, self.right] if x is not None]
        if len(v) == 1:
            return v[0]
        else:
            return f"Concat({', '.join(v)})"

    __repr__ = __str__

    def execute(self, data):
        l = self.left
        r = self.right
        o = self.op

        if isinstance(l, OpTree):
            l = l.execute(data)
        elif l is not None:
            l = l(data).execute()
        else:
            l = ''

        if isinstance(r, OpTree):
            r = r.execute(data)
        elif r is not None:
            r = r(data).execute()
        else:
            r = ''

        assert not isinstance(o, OpTree)

        return l + o(data).execute() + r

def LeftRemainder(O, P):
    # prefix of O before P
    # assuming unique ?
    out = []
    is_empty = True
    for o, p in zip(O, P):
        n = o.find(p)
        if n != -1:
            out.append(o[:n])
            is_empty = is_empty and len(out[-1]) == 0
        #else:
        #    out.append(o)

    return out, is_empty

def RightRemainder(O, P):
    # suffix of O after P
    out = []
    is_empty = True
    for o, p in zip(O, P):
        n = o.find(p)
        if n != -1:
            out.append(o[n+len(p):])
            is_empty = is_empty and len(out[-1]) == 0
        #else:
        #    out.append(o)

    return out, is_empty

def ngrams(s, n):
    out = []
    for i in range(len(s) - n):
        out.append(s[i:i+n])

    return out

class Op:
    def __init__(self, cls, *args):
        self.cls = cls
        self.args = args

    def __str__(self):
        if self.cls is Constant:
            return repr(self.cls(*self.args))
        else:
            return repr(self.cls("ROW", *self.args))

    __repr__ = __str__

    def get_lambda(self):
        if self.cls is Constant:
            return lambda _: self.cls(*self.args)
        else:
            return lambda x: self.cls(x, *self.args)
