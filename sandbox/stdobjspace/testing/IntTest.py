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

    def intTest(self):
        f1 = iobj.W_IntObject(1.0)
        result = iobj.int_int(self.space,f1)
        assert result == f1

    def reprTest(self):
        x = 1.0
        f1 = iobj.W_IntObject(x)
        result = iobj.int_repr(self.space,f1)
        assert result == repr(x)

    def strTest(self):
        x = 1.0
        f1 = iobj.W_IntObject(x)
        result = iobj.int_str(self.space,f1)
        assert result == str(x)

    def hashTest(self):
        x = 1.0
        f1 = iobj.W_IntObject(x)
        result = iobj.int_hash(self.space,f1)
        assert result == hash(x)

    def addTest(self):
        f1 = iobj.W_IntObject(1.0)
        f2 = iobj.W_IntObject(2.0)
        result = iobj.int_int_add(self.space,f1,f2)
        assert result.intval == 3.0

    def subTest(self):
        f1 = iobj.W_IntObject(1.0)
        f2 = iobj.W_IntObject(2.0)
        result = iobj.int_int_sub(self.space,f1,f2)
        assert result.intval == -1.0

    def mulTest(self):
        f1 = iobj.W_IntObject(1.0)
        f2 = iobj.W_IntObject(2.0)
        result = iobj.int_int_mul(self.space,f1,f2)
        assert result.intval == 2.0

    def divTest(self):
        f1 = iobj.W_IntObject(1.0)
        f2 = iobj.W_IntObject(2.0)
        result = iobj.int_int_div(self.space,f1,f2)
        assert result.intval == 0.5

    def modTest(self):
        x = 1.0
        y = 2.0
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_mod(self.space,f1,f2)
        assert v.intval == x % y

    def divmodTest(self):
        x = 1.0
        y = 2.0
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v,w = iobj.int_int_divmod(self.space,f1,f2)
        assert (v.intval,w.intval) == divmod(x,y)

    def powTest(self):
        x = 1.0
        y = 2.0
        f1 = iobj.W_IntObject(x)
        f2 = iobj.W_IntObject(y)
        v = iobj.int_int_pow(self.space,f1,f2)
        assert v.intval == x ** y


def makeTestSuite():
    suiteAtomic = unittest.TestSuite()
    suiteAtomic.addTest(intTest('intTest'))
    suiteAtomic.addTest(intTest('reprTest'))
    suiteAtomic.addTest(intTest('strTest'))
    suiteAtomic.addTest(intTest('hashTest'))
    suiteAtomic.addTest(intTest('addTest'))
    suiteAtomic.addTest(intTest('subTest'))
    suiteAtomic.addTest(intTest('mulTest'))
    suiteAtomic.addTest(intTest('divTest'))
    suiteAtomic.addTest(intTest('modTest'))
    suiteAtomic.addTest(intTest('divmodTest'))
    suiteAtomic.addTest(intTest('powTest'))

    return unittest.TestSuite((suiteAtomic,))

def main():
    os.chdir("..")
    print os.getcwd()
    unittest.main(defaultTest='makeTestSuite')
    print os.getcwd()
    os.chdir(thisdir)
    print os.getcwd()

if __name__ == '__main__':
    main()
