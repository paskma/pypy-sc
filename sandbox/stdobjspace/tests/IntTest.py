#!/usr/bin/env python
import sys
import os
import objspace
thisdir = os.getcwd()
sys.path.insert(0, thisdir)
os.chdir('..')
syspath = sys.path
sys.path.append(os.getcwd())

import unittest

#######################################
# import the module you want to test
# import yourmodule
#######################################

import intobject as iobj

os.chdir(thisdir)
sys.path = syspath

class intTest(unittest.TestCase):

    def setUp(self):
        self.space = objspace.StdObjSpace

    def tearDown(self):
        pass

    def _longshiftresult(self, x):
        """ calculate an overflowing shift """
        n = 1
        l = long(x)
        while 1:
            ires = x << n
            lres = l << n
            if type(ires) is long or lres != ires:
                return n
            n += 1

    def _unwrap_nonimpl(self, func, *args, **kwds):
        """ make sure that the expected exception occours, and unwrap it """
        try:
            res = func(*args, **kwds)
            raise Exception, "should have failed but returned '%s'!" %repr(res)
        except objspace.FailedToImplement, arg:
            return arg[0]

    def _unwrap_except(self, func, *args, **kwds):
        """ make sure that the expected exception occours, and unwrap it """
        try:
            res = func(*args, **kwds)
            raise Exception, "should have failed but returned '%s'!" %repr(res)
        except objspace.OperationError, arg:
            return arg[0]

    def test_repr(self):
        x = 1
        f1 = iobj.W_IntObject(x)
        result = iobj.int_repr(self.space, f1)
        self.assertEquals(self.space.unwrap(result), repr(x))

    def test_str(self):
        x = 12345
        f1 = iobj.W_IntObject(x)
        result = iobj.int_str(self.space, f1)
        self.assertEquals(self.space.unwrap(result), str(x))

    def test_hash(self):
        x = 42
        f1 = iobj.W_IntObject(x)
        result = iobj.int_hash(self.space, f1)
        self.assertEquals(result.intval, hash(x))

    def test_add(self):
        x = 1
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        result = iobj.int_int_add(self.space, f1, f2)
        self.assertEquals(result.intval, x+y)
        x = sys.maxint
        y = 1
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_add, self.space, f1, f2))

    def test_sub(self):
        x = 1
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        result = iobj.int_int_sub(self.space, f1, f2)
        self.assertEquals(result.intval, x-y)
        x = sys.maxint
        y = -1
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_sub, self.space, f1, f2))


    def test_mul(self):
        x = 2
        y = 3
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        result = iobj.int_int_mul(self.space, f1, f2)
        self.assertEquals(result.intval, x*y)
        x = -sys.maxint-1
        y = -1
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_mul, self.space, f1, f2))


    def test_div(self):
        for i in range(10):
            res = i//3
            f1 = iobj.W_IntObject(i)
            f2 = iobj.W_IntObject(3)
            result = iobj.int_int_div(self.space, f1, f2)
            self.assertEquals(result.intval, res)
        x = -sys.maxint-1
        y = -1
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_div, self.space, f1, f2))

    def test_mod(self):
        x = 1
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_mod(self.space, f1, f2)
        self.assertEquals(v.intval, x % y)
        # not that mod cannot overflow

    def test_divmod(self):
        x = 1
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        ret = iobj.int_int_divmod(self.space, f1, f2)
        v, w = self.space.unwrap(ret)
        self.assertEquals((v.intval, w.intval), divmod(x, y))
        x = -sys.maxint-1
        y = -1
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_divmod, self.space, f1, f2))

    def test_pow_iii(self):
        x = 10
        y = 2
        z = 13
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        f3 = iobj.W_IntObject(z)
        v = iobj.int_int_int_pow(self.space, f1, f2, f3)
        self.assertEquals(v.intval, pow(x, y, z))
        f1, f2, f3 = map(iobj.W_IntObject, (10, -1, 42))
        self.assertEquals(self.space.w_TypeError,
                          self._unwrap_except(iobj.int_int_int_pow, self.space, f1, f2, f3))
        f1, f2, f3 = map(iobj.W_IntObject, (10, 5, 0))
        self.assertEquals(self.space.w_ValueError,
                          self._unwrap_except(iobj.int_int_int_pow, self.space, f1, f2, f3))

    def test_pow_iin(self):
        x = 10
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_none_pow(self.space, f1, f2)
        self.assertEquals(v.intval, x ** y)
        f1, f2 = map(iobj.W_IntObject, (10, 20))
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_none_pow, self.space, f1, f2))
        f1, f2 = map(iobj.W_IntObject, (10, -1))
        self.assertEquals(self.space.w_ValueError,
                          self._unwrap_nonimpl(iobj.int_int_none_pow, self.space, f1, f2))

    def test_neg(self):
        x = 42
        f1 = iobj.W_IntObject(x)
        v = iobj.int_neg(self.space, f1)
        self.assertEquals(v.intval, -x)
        x = -sys.maxint-1
        f1 = iobj.W_IntObject(x)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_neg, self.space, f1))

    def test_pos(self):
        x = 42
        f1 = iobj.W_IntObject(x)
        v = iobj.int_pos(self.space, f1)
        self.assertEquals(v.intval, +x)

    def test_abs(self):
        x = 42
        f1 = iobj.W_IntObject(x)
        v = iobj.int_abs(self.space, f1)
        self.assertEquals(v.intval, abs(x))
        x = -42
        f1 = iobj.W_IntObject(x)
        v = iobj.int_abs(self.space, f1)
        self.assertEquals(v.intval, abs(x))
        x = -sys.maxint-1
        f1 = iobj.W_IntObject(x)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_neg, self.space, f1))

    def test_pos(self):
        x = 42
        f1 = iobj.W_IntObject(x)
        v = iobj.int_invert(self.space, f1)
        self.assertEquals(v.intval, ~x)

    def test_lshift(self):
        x = 12345678
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_lshift(self.space, f1, f2)
        self.assertEquals(v.intval, x << y)
        y = self._longshiftresult(x)
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        self.assertEquals(self.space.w_OverflowError,
                          self._unwrap_nonimpl(iobj.int_int_lshift, self.space, f1, f2))

    def test_rshift(self):
        x = 12345678
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_rshift(self.space, f1, f2)
        self.assertEquals(v.intval, x >> y)

    def test_and(self):
        x = 12345678
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_and(self.space, f1, f2)
        self.assertEquals(v.intval, x & y)

    def test_xor(self):
        x = 12345678
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_xor(self.space, f1, f2)
        self.assertEquals(v.intval, x ^ y)

    def test_or(self):
        x = 12345678
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_or(self.space, f1, f2)
        self.assertEquals(v.intval, x | y)

    def test_int(self):
        f1 = iobj.W_IntObject(1)
        result = iobj.int_int(self.space, f1)
        self.assertEquals(result, f1)

    def test_long(self):
        x = 1
        f1 = iobj.W_IntObject(x)
        result = iobj.int_long(self.space, f1)
        self.assertEquals(self.space.unwrap(result), long(x))

    def test_float(self):
        x = 1
        f1 = iobj.W_IntObject(x)
        result = iobj.int_float(self.space, f1)
        self.assertEquals(self.space.unwrap(result), float(x))

    def test_oct(self):
        x = 012345
        f1 = iobj.W_IntObject(x)
        result = iobj.int_oct(self.space, f1)
        self.assertEquals(self.space.unwrap(result), oct(x))

    def test_hex(self):
        x = 0x12345
        f1 = iobj.W_IntObject(x)
        result = iobj.int_hex(self.space, f1)
        self.assertEquals(self.space.unwrap(result), hex(x))

def makeTestSuite():
    suiteAtomic = unittest.TestSuite()
    loader = unittest.TestLoader()
    suiteAtomic.addTest(loader.loadTestsFromTestCase(intTest))
    return suiteAtomic

def main():
    os.chdir("..")
    unittest.TextTestRunner().run(makeTestSuite())
    os.chdir(thisdir)

if __name__ == '__main__':
    main()
