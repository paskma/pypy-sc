class r_int(int):
    """ fake integer implementation in order to make sure that
    primitive integer operations do overflow """

    def __add__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x+y)
    __radd__ = __add__
    
    def __sub__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x-y)
    __rsub__ = __sub__
    
    def __mul__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x*y)
    __rmul__ = __mul__

    def __div__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x//y)
    __rdiv__ = __div__

    __floordiv__ = __rfloordiv__ = __div__

    def __lshift__(self, n):
        # ensure long shift, so we don't depend on
        # shift truncation (2.3) vs. long(2.4)
        x = long(self)
        y = int(n)
        return r_int(x << y)
    __rlshift__ = __lshift__

    def __rshift__(self, n):
        x = int(self)
        y = int(n)
        return r_int(x >> y)
    __rrshift__ = __rshift__

    def __or__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x|y)
    __ror__ = __or__

    def __and__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x&y)
    __rand__ = __and__

    def __xor__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x^y)
    __rxor__ = __xor__

    def __neg__(self):
        x = int(self)
        return r_int(-x)

    def __pos__(self):
        return r_int(self)

    def __not__(self):
        x = int(self)
        return r_int(~x)

    def __pow__(self, other, m=None):
        x = int(self)
        res = pow(x, other, m)
        return r_int(res)
    __rpow__ = __pow__

    def __divmod__(self, other):
        res = divmod(self, other)
        return r_int(res)

    