import unittest, sys, os
sys.path.insert(0, '..')

from pyframe import PyFrame
import trivialspace, executioncontext


class TestExecutionContext(unittest.TestCase):

    def test_trivial1(self):
        # build frame
        space = trivialspace.TrivialSpace()
        ec = executioncontext.ExecutionContext(space)
        
        bytecode = compile('def f(x): return x+1', '', 'exec').co_consts[0]
        w_globals = ec.make_standard_w_globals()
        w_locals = space.newdict([])
        frame = PyFrame(space, bytecode, w_globals, w_locals)
        w_input = frame.space.wrap((5,))
        frame.setargs(w_input)
        w_output = ec.eval_frame(frame)
        self.assertEquals(frame.space.unwrap(w_output), 6)


if __name__ == '__main__':
    unittest.main()
