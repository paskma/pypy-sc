import sys

class ExecutionContext:

    def __init__(self, space):
        self.space = space
        self.framestack = []

    def eval_frame(self, frame):
        __executioncontext__ = self
        self.framestack.append(frame)
        try:
            result = frame.eval(self)
        finally:
            self.framestack.pop()
        return result

    def get_w_builtins(self):
        if self.framestack:
            return self.framestack[-1].w_builtins
        else:
            return self.space.w_builtins

    def make_standard_w_globals(self):
        "Create a new empty 'globals' dictionary."
        w_key = self.space.wrap("__builtins__")
        w_value = self.get_w_builtins()
        w_globals = self.space.newdict([(w_key, w_value)])
        return w_globals

    def exception_trace(self, operationerr):
        "Trace function called upon OperationError."
        import sys, traceback
        tb = sys.exc_info()[2]
        w_exc, w_value = operationerr.args
        exc = self.space.unwrap(w_exc)
        value = self.space.unwrap(w_value)
        print >> sys.stderr, "*"*10, " OperationError ", "*"*10
        traceback.print_tb(tb)
        msg = traceback.format_exception_only(exc, value)
        print >> sys.stderr, "[Application-level]", ''.join(msg).strip()
        print >> sys.stderr, "*"*10
