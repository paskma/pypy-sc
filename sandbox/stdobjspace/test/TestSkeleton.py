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
# import the module you want to test here
# import yourmodule
#######################################

True,False = (1==1),(1==0)

class SomeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def someTest(self):
        pass


def makeTestSuite():
    suiteAtomic = unittest.TestSuite()
    suiteAtomic.addTest(SomeTest('someTest'))

    return unittest.TestSuite((suiteAtomic,))

def main():
    unittest.main(defaultTest='makeTestSuite')
    sys.path = syspath
    os.chdir(thispath)

if __name__ == '__main__':
    main()
