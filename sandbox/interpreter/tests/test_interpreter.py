import unittest, sys, os
sys.path.insert(0, '..')

from pyframe import PyFrame
import objectspace, trivialspace, executioncontext


def testcode(code, functionname, args):
    bytecode = compile(code, '<test>', 'exec')

    space = trivialspace.TrivialSpace()
    apphelper = objectspace.AppHelper(space, bytecode)
    
    wrappedargs = [space.wrap(arg) for arg in args]
    w_output = apphelper.call(functionname, wrappedargs)
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

    def test_identity(self):
        x = testcode('''
def g(x): return x''', 'g', [666])
        self.assertEquals(x, 666)

    def test_exception(self):
        x = testcode('''
def f():
    try:
        raise Exception, 1
    except Exception, e:
        return e.args[0]
''', 'f', [])
        self.assertEquals(x, 1)



if __name__ == '__main__':
    unittest.main()
