from pyframe import PyFrame
import trivialspace


space = trivialspace
src = open('test1-source.py', 'r').read()
bytecode = compile(src, 'test1-source', 'exec').co_consts[1]
w_globals = space.wrap({'__builtins__': __builtins__})
w_locals = space.wrap({})
frame = PyFrame(space, bytecode, w_globals, w_locals)


def test(frame):
    w_input = frame.space.wrap((5,))
    frame.setargs(w_input)
    w_output = frame.eval()
    assert frame.space.unwrap(w_output) == 6

test(frame)
