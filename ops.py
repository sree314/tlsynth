from enum import Enum

class POperator:
    def _e(self, v):
        # type safety?
        if isinstance(v, str):
            return v
        elif isinstance(v, (list, tuple)):
            return v
        elif isinstance(v, int):
            return v
        elif isinstance(v, POperator):
            return v.execute()
        else:
            raise NotImplementedError(v)

class Nop(POperator):
    def execute(self):
        return ""

class Split(POperator):
    def __init__(self, v, sep):
        self.v = v
        self.sep = sep

    def __str__(self):
        return f"Split({repr(self.v)}, {repr(self.sep)})"

    __repr__ = __str__

    def execute(self):
        spl = self._e(self.v).split(self._e(self.sep), 1) # This seems to only split into two
        if len(spl) == 1:
            spl.append('') #hack

        return spl

class SelectK(POperator):
    def __init__(self, arr, k):
        self.arr = arr
        self.k = k

    def __str__(self):
        return f"SelectK({repr(self.arr)}, {repr(self.k)})"

    __repr__ = __str__

    def execute(self):
        return self._e(self.arr)[self._e(self.k)]

class Concat(POperator):
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __str__(self):
        return f"Concat({repr(self.u)}, {repr(self.v)})"

    __repr__ = __str__

    def execute(self):
        return self._e(self.u) + self._e(self.v)

class Constant(POperator):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return f"Constant({repr(self.v)})"

    __repr__ = __str__

    def execute(self):
        return self._e(self.v)

    def solve(self, I, O):
        x = set(O)
        if len(x) == 1:
            return Constant(x.pop())

        return None

class Case(Enum):
    UNCHANGED = 0
    UPPER = 1
    LOWER = 2

class Substring(POperator):
    def __init__(self, v, start, length, c = None):
        self.v = v
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"Substring({repr(self.v)}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        v = self._e(self.v)
        if self.length == -1:
            l = len(v)
        else:
            l = self.length

        x = v[self.start:self.start+l]

        if self.c is not None and self.c != Case.UNCHANGED:
            if self.c == Case.UPPER:
                x = x.upper()
            elif self.c == Case.LOWER:
                x = x.lower()
            else:
                raise NotImplementedError(self.c)

        return x

class LOperator(POperator):
    pass

class SplitSubstr(LOperator):
    def __init__(self, arr, k, sep, m, start, length, c):
        self.arr = arr
        self.k = k
        self.sep = sep
        self.m = m
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"SplitSubstr({self.arr}, {self.k}, {repr(self.sep)}, {self.m}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        return Substring(SelectK(Split(SelectK(self.arr, self.k), self.sep), self.m),
                         self.start, self.length, self.c).execute()

class SplitSplitSubstr(LOperator):
    def __init__(self, arr, k1, sep1, k2, sep2, m, start, length, c):
        self.arr = arr
        self.k1 = k1
        self.sep1 = sep1
        self.k2 = k2
        self.sep2 = sep2
        self.m = m
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"SplitSplitSubstr({self.arr}, {self.k1}, {repr(self.sep1)}, {self.k2}, {repr(self.sep2)}, {self.m}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        return Substring(SelectK(Split(SelectK(Split(SelectK(self.arr,
                                                             self.k1), self.sep1),
                                               self.k2), self.sep2), self.m),
                         self.start, self.length, self.c).execute()


class Substr(LOperator):
    def __init__(self, arr, m, start, length, c):
        self.arr = arr
        self.m = m
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"Substr({self.arr}, {self.m}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        return Substring(SelectK(self.arr, self.m), self.start, self.length, self.c).execute()

class POperator:
    def _e(self, v):
        # type safety?
        if isinstance(v, str):
            return v
        elif isinstance(v, (list, tuple)):
            return v
        elif isinstance(v, int):
            return v
        elif isinstance(v, POperator):
            return v.execute()
        else:
            raise NotImplementedError(type(v))

class Nop(POperator):
    def execute(self):
        return ""

class Split(POperator):
    def __init__(self, v, sep):
        self.v = v
        self.sep = sep

    def __str__(self):
        return f"Split({repr(self.v)}, {repr(self.sep)})"

    __repr__ = __str__

    def execute(self):
        spl = self._e(self.v).split(self._e(self.sep), 1) # This seems to only split into two
        if len(spl) == 1:
            spl.append('') #hack

        return spl

class SelectK(POperator):
    def __init__(self, arr, k):
        self.arr = arr
        self.k = k

    def __str__(self):
        return f"SelectK({repr(self.arr)}, {repr(self.k)})"

    __repr__ = __str__

    def execute(self):
        return self._e(self.arr)[self._e(self.k)]

class Concat(POperator):
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __str__(self):
        return f"Concat({repr(self.u)}, {repr(self.v)})"

    __repr__ = __str__

    def execute(self):
        return self._e(self.u) + self._e(self.v)

class Constant(POperator):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return f"Constant({repr(self.v)})"

    __repr__ = __str__

    def execute(self):
        return self._e(self.v)

    def solve(self, I, O):
        x = set(O)
        if len(x) == 1:
            return Constant(x.pop())

        return None

class Case(Enum):
    UNCHANGED = 0
    UPPER = 1
    LOWER = 2

class Substring(POperator):
    def __init__(self, v, start, length, c = None):
        self.v = v
        self.start = start
        self.length = length
        self.c = c # TODO

    def __str__(self):
        return f"Substring({repr(self.v)}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        v = self._e(self.v)
        if self.length == -1:
            l = len(v)
        else:
            l = self.length

        x = v[self.start:self.start+l]

        if self.c is not None and self.c != Case.UNCHANGED:
            if self.c == Case.UPPER:
                x = x.upper()
            elif self.c == Case.LOWER:
                x = x.lower()
            else:
                raise NotImplementedError(self.c)

        return x

class LOperator(POperator):
    pass

class SplitSubstr(LOperator):
    def __init__(self, arr, k, sep, m, start, length, c):
        self.arr = arr
        self.k = k
        self.sep = sep
        self.m = m
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"SplitSubstr({self.arr}, {self.k}, {repr(self.sep)}, {self.m}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        return Substring(SelectK(Split(SelectK(self.arr, self.k), self.sep), self.m),
                         self.start, self.length, self.c).execute()

class SplitSplitSubstr(LOperator):
    def __init__(self, arr, k1, sep1, k2, sep2, m, start, length, c):
        self.arr = arr
        self.k1 = k1
        self.sep1 = sep1
        self.k2 = k2
        self.sep2 = sep2
        self.m = m
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"SplitSplitSubstr({self.arr}, {self.k1}, {repr(self.sep1)}, {self.k2}, {repr(self.sep2)}, {self.m}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        return Substring(SelectK(Split(SelectK(Split(SelectK(self.arr,
                                                             self.k1), self.sep1),
                                               self.k2), self.sep2), self.m),
                         self.start, self.length, self.c).execute()


class Substr(LOperator):
    def __init__(self, arr, m, start, length, c):
        self.arr = arr
        self.m = m
        self.start = start
        self.length = length
        self.c = c

    def __str__(self):
        return f"Substr({self.arr}, {self.m}, {self.start}, {self.length}, {self.c})"

    __repr__ = __str__

    def execute(self):
        return Substring(SelectK(self.arr, self.m), self.start, self.length, self.c).execute()
