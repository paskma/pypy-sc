import unittest, sys, os
sys.path.insert(0, '..')

from pyframe import PyFrame
import objectspace, trivialspace, executioncontext


def testcode(code, functionname, args):
    helperbytecode = objectspace.HelperBytecode(code, '<test>')

    space = trivialspace.TrivialSpace()
    wrappedargs = [space.wrap(arg) for arg in args]
    w_output = space.gethelper(helperbytecode).call(functionname, wrappedargs)
    return space.unwrap(w_output)


class TestInterpreter(unittest.TestCase):

    def test_trivial(self):
        x = testcode('''
def g(): return 42''', 'g', [])
        self.assertEquals(x, 42)

    def test_trivial_call(self):
        x = testcode('''
def f(): return 42
def g(): return f()''', 'g', [])
        self.assertEquals(x, 42)

    def test_trivial_call2(self):
        x = testcode('''
def f(): return 1 + 1
def g(): return f()''', 'g', [])
        self.assertEquals(x, 2)

    def test_print(self):
        x = testcode('''
def g(): print 10''', 'g', [])
        self.assertEquals(x, None)

if __name__ == '__main__':
    unittest.main()
