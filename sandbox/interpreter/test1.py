from pypy import PyFrame, BorrowObjectSpace



space = BorrowObjectSpace()
src = open('test1-source.py', 'r').read()
bytecode = compile(src, 'test1-source', 'exec').co_consts[1]
v_globals = space.wrap({})
v_locals = space.wrap({})
frame = PyFrame(space, bytecode, v_globals, v_locals)



def test(frame):
    v_input = frame.space.wrap((5,))
    frame.setargs(v_input)
    v_output = frame.eval()
    assert frame.space.unwrap(v_output) == 6


test(frame)



