from pypy.objspace.std.objspace import *
import pypy.interpreter.pyframe


class W_FuncObject(object):
    def __init__(self, w_code, w_globals, w_defaultarguments, w_closure):
        self.w_code = w_code
        self.w_globals = w_globals
        self.w_defaultarguments = w_defaultarguments
        self.w_closure = w_closure


def func_call(space, w_function, w_arguments, w_keywords):
    ec = space.getexecutioncontext()
    bytecode = space.unwrap(self.w_code)
    w_locals = space.newdict([])
    frame = pypy.interpreter.pyframe.PyFrame(space, bytecode,
                                             self.w_globals, w_locals)
    frame.setargs(w_arguments, w_keywords,
                  w_defaults = w_defaultarguments,
                  w_closure = w_closure)
    return ec.eval_frame(frame)
