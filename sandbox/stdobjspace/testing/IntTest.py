#!/usr/bin/env python
import sys
import os
import objspace
thisdir = os.getcwd()
sys.path.insert(0,thisdir)
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

    def test_int(self):
        f1 = iobj.W_IntObject(1)
        result = iobj.int_int(self.space,f1)
        assert result == f1

    def test_repr(self):
        x = 1
        f1 = iobj.W_IntObject(x)
        result = iobj.int_repr(self.space,f1)
        assert result == repr(x)

    def test_str(self):
        x = 1
        f1 = iobj.W_IntObject(x)
        result = iobj.int_str(self.space,f1)
        assert result == str(x)

    def test_hash(self):
        x = 1
        f1 = iobj.W_IntObject(x)
        result = iobj.int_hash(self.space,f1)
        assert result == hash(x)

    def test_add(self):
        f1 = iobj.W_IntObject(1)
        f2 = iobj.W_IntObject(2)
        result = iobj.int_int_add(self.space,f1,f2)
        assert result.intval == 3.0

    def test_sub(self):
        f1 = iobj.W_IntObject(1)
        f2 = iobj.W_IntObject(2)
        result = iobj.int_int_sub(self.space,f1,f2)
        assert result.intval == -1

    def test_mul(self):
        f1 = iobj.W_IntObject(1)
        f2 = iobj.W_IntObject(2)
        result = iobj.int_int_mul(self.space,f1,f2)
        assert result.intval == 2

    def test_div(self):
        f1 = iobj.W_IntObject(1)
        f2 = iobj.W_IntObject(2)
        result = iobj.int_int_div(self.space,f1,f2)
        assert result.intval == 0.5

    def test_mod(self):
        x = 1
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_mod(self.space,f1,f2)
        assert v.intval == x % y

    def test_divmod(self):
        x = 1
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v,w = iobj.int_int_divmod(self.space,f1,f2)
        assert (v.intval,w.intval) == divmod(x,y)

    def test_pow_iii(self):
        x = 10
        y = 2
        z = 13
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        f3 = iobj.W_IntObject(z)
        v = iobj.int_int_int_pow(self.space, f1, f2, f3)
        assert v.intval == pow(x, y, z)

    def test_pow_iin(self):
        x = 10
        y = 2
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_none_pow(self.space,f1,f2)
        assert v.intval == x ** y

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
