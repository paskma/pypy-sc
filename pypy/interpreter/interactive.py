from pypy.interpreter import executioncontext
from pypy.interpreter import pyframe
from pypy.objspace import trivial
import code

class PyPyConsole(code.InteractiveConsole):
    def __init__(self):
        code.InteractiveConsole.__init__(self)
        self.space = trivial.TrivialObjSpace()
        self.ec = executioncontext.ExecutionContext(self.space)
        self.locals['__builtins__'] = self.space.w_builtins

    def runcode(self, code):
        # ah ha!
        frame = pyframe.PyFrame(self.space, code,
                        self.locals, self.locals)
        self.ec.eval_frame(frame)
        
if __name__ == '__main__':
    con = PyPyConsole()
    con.interact()

