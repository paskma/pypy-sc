import unittest, sys, os
sys.path.insert(0, '..')

from pyframe import PyFrame
import trivialspace


class TestExecutionContext(unittest.TestCase):

    def test_trivial1(self):
        # build frame
        space = TrivialSpace()

        ec = ExecutionContext(space)

        space.initialize(ec)
        
        bytecode = compile('def f(x): return x+1', '', 'exec').co_consts[0]
        w_globals = space.wrap({'__builtins__': __builtins__})
        w_locals = space.wrap({})
        frame = PyFrame(space, bytecode, w_globals, w_locals)
        w_input = frame.space.wrap((5,))
        frame.setargs(w_input)
        w_output = ec.eval_frame(frame)
        self.assertEquals(frame.space.unwrap(w_output), 6)


if __name__ == '__main__':
    unittest.main()
