import unittest
import testsupport


def testcode(code, functionname, args, space=None):
    """Compile and run the given code string, and then call its function
    named by 'functionname' with arguments 'args'.
    The optional 'space' argument can specify an alternate object space."""
    from interpreter.pyframe import PyFrame
    from interpreter import baseobjspace, executioncontext
    if space is None:
        from objspace.trivial import TrivialObjSpace
        space = TrivialObjSpace()

    bytecode = compile(code, '<test>', 'exec')
    apphelper = baseobjspace.AppHelper(space, bytecode)
    
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

    def test_finally(self):
        code = '''
def f(a):
    try:
        if a:
            raise Exception
    finally:
        return 2
'''
        self.assertEquals(testcode(code, 'f', [0]), 2)
        self.assertEquals(testcode(code, 'f', [1]), 2)


if __name__ == '__main__':
    unittest.main()
