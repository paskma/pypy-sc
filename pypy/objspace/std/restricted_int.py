"""
This file defines restricted integers.

Purpose:
Have an integer implementation that emulates
restricted Python for CPython.

r_int   an integer type which has overflow checking.
        It doesn not automatically extend to long
r_uint  an unsigned integer which has not overflow
        checking. It is always positive and always
        truncated to the internal machine word size.

We try to keep the number of such internal types
to a minimum.
"""

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

    def __mod__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x % y)
    __rmod__ = __mod__

    def __divmod__(self, other):
        res = divmod(self, other)
        return tuple(r_int(res[0]), r_int(res[1]))

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
        return r_int(x | y)
    __ror__ = __or__

    def __and__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x & y)
    __rand__ = __and__

    def __xor__(self, other):
        x = int(self)
        y = int(other)
        return r_int(x ^ y)
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

# set up of machine internals
_bits = 0
_itest = 1
_Ltest = 1L
while _itest == _Ltest and type(_itest) is int:
    _itest <<= 1
    _Ltest <<= 1
    _bits += 1

LONG_BIT = _bits+1
LONG_MASK = _Ltest*2-1

del _bits, _itest, _Ltest

class r_uint(long):
    """ fake unsigned integer implementation """

    _mask = LONG_MASK

    def __new__(klass, val):
        return long.__new__(klass, val & klass._mask)

    def __add__(x, y):
        return r_uint(x + y)
    __radd__ = __add__
    
    def __sub__(x, y):
        return r_uint(x - y)
    __rsub__ = __sub__
    
    def __mul__(x, y):
        return r_uint(x * y)
    __rmul__ = __mul__

    def __div__(x, y):
        return r_uint(x // y)
    __rdiv__ = __div__

    __floordiv__ = __rfloordiv__ = __div__

    def __mod__(x, y):
        return r_uint(x % y)
    __rmod__ = __mod__

    def __divmod__(x, y):
        res = divmod(x, y)
        return tuple(r_uint(res[0]), r_uint(res[1]))

    def __lshift__(x, y):
        return r_uint(x << y)
    __rlshift__ = __lshift__

    def __rshift__(x, y):
        return r_uint(x >> y)
    __rrshift__ = __rshift__

    def __or__(x, y):
        return r_uint(x | y)
    __ror__ = __or__

    def __and__(x, y):
        return r_uint(x & y)
    __rand__ = __and__

    def __xor__(x, y):
        return r_uint(x^y)
    __rxor__ = __xor__

    def __neg__(x):
        return r_uint(-x)

    def __pos__(self):
        return r_uint(self)

    def __not__(x):
        return r_uint(~x)

    def __pow__(x, y, m=None):
        res = pow(x, y, m)
        return r_uint(res)
    __rpow__ = __pow__
