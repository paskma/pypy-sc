#!/usr/bin/env python
import sys
import os
import objspace
thisdir = os.getcwd()
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

    def addTest(self):
        f1 = fl.W_FloatObject(1.0)
        f2 = fl.W_FloatObject(2.0)
        result = fl.float_float_add(self.space,f1,f2)
        assert result.floatval == 3.0

    def divmodTest(self):
        x = 1.0
        y = 2.0
        f1 = fl.W_FloatObject(x)
        f2 = fl.W_FloatObject(y)
        v,w = fl.float_float_divmod(self.space,f1,f2)
        assert (v,w) == divmod(x,y)


def makeTestSuite():
    suiteAtomic = unittest.TestSuite()
    suiteAtomic.addTest(floatTest('addTest'))
    suiteAtomic.addTest(floatTest('divmodTest'))

    return unittest.TestSuite((suiteAtomic,))

def main():
    unittest.main(defaultTest='makeTestSuite')

if __name__ == '__main__':
    main()
