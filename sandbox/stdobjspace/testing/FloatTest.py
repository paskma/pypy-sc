#!/usr/bin/env python
import sys
import os
import objspace
thisdir = os.getcwd()
syspath = sys.path
sys.path.insert(0,thisdir)
sys.path.append('..')
import unittest

os.chdir('..')

#######################################
# import the module you want to test
# import yourmodule
#######################################

import floatobject as fl

True,False = (1==1),(1==0)

class floatTest(unittest.TestCase):

    def setUp(self):
        self.space = objspace.StdObjSpace

    def tearDown(self):
        pass

    def floatTest(self):
        f1 = fl.W_FloatObject(1.0)
        result = fl.float_float(self.space,f1)
        assert result == f1

    def reprTest(self):
        x = 1.0
        f1 = fl.W_FloatObject(x)
        result = fl.float_repr(self.space,f1)
        assert result == repr(x)

    def strTest(self):
        x = 1.0
        f1 = fl.W_FloatObject(x)
        result = fl.float_str(self.space,f1)
        assert result == str(x)

    def hashTest(self):
        x = 1.0
        f1 = fl.W_FloatObject(x)
        result = fl.float_hash(self.space,f1)
        assert result == hash(x)

    def addTest(self):
        f1 = fl.W_FloatObject(1.0)
        f2 = fl.W_FloatObject(2.0)
        result = fl.float_float_add(self.space,f1,f2)
        assert result.floatval == 3.0

    def subTest(self):
        f1 = fl.W_FloatObject(1.0)
        f2 = fl.W_FloatObject(2.0)
        result = fl.float_float_sub(self.space,f1,f2)
        assert result.floatval == -1.0

    def mulTest(self):
        f1 = fl.W_FloatObject(1.0)
        f2 = fl.W_FloatObject(2.0)
        result = fl.float_float_mul(self.space,f1,f2)
        assert result.floatval == 2.0

    def divTest(self):
        f1 = fl.W_FloatObject(1.0)
        f2 = fl.W_FloatObject(2.0)
        result = fl.float_float_div(self.space,f1,f2)
        assert result.floatval == 0.5

    def modTest(self):
        x = 1.0
        y = 2.0
        f1 = fl.W_FloatObject(x)
        f2 = fl.W_FloatObject(y)
        v = fl.float_float_mod(self.space,f1,f2)
        assert v.floatval == x % y

    def divmodTest(self):
        x = 1.0
        y = 2.0
        f1 = fl.W_FloatObject(x)
        f2 = fl.W_FloatObject(y)
        v,w = fl.float_float_divmod(self.space,f1,f2)
        assert (v.floatval,w.floatval) == divmod(x,y)

    def powTest(self):
        x = 1.0
        y = 2.0
        f1 = fl.W_FloatObject(x)
        f2 = fl.W_FloatObject(y)
        v = fl.float_float_pow(self.space,f1,f2)
        assert v.floatval == x ** y


def makeTestSuite():
    suiteAtomic = unittest.TestSuite()
    suiteAtomic.addTest(floatTest('floatTest'))
    suiteAtomic.addTest(floatTest('reprTest'))
    suiteAtomic.addTest(floatTest('strTest'))
    suiteAtomic.addTest(floatTest('hashTest'))
    suiteAtomic.addTest(floatTest('addTest'))
    suiteAtomic.addTest(floatTest('subTest'))
    suiteAtomic.addTest(floatTest('mulTest'))
    suiteAtomic.addTest(floatTest('divTest'))
    suiteAtomic.addTest(floatTest('modTest'))
    suiteAtomic.addTest(floatTest('divmodTest'))
    suiteAtomic.addTest(floatTest('powTest'))

    return unittest.TestSuite((suiteAtomic,))

def main():
    unittest.main(defaultTest='makeTestSuite')
    sys.path = syspath
    os.chdir(thispath)

if __name__ == '__main__':
    main()
