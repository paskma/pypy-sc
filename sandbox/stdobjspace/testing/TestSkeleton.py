#!/usr/bin/env python
import sys

sys.path.append('..')

import unittest

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

if __name__ == '__main__':
    main()
