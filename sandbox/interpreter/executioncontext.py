import sys


class ExecutionContext:

    def __init__(self, space):
        self.space = space
        self.framestack = []

    def eval_frame(self, frame):
        __executioncontext__ = self
        self.framestack.append(frame)
        try:
            result = frame.eval()
        finally:
            self.framestack.pop()


# Public
def getexecutioncontext():
    return dynamic_get('__executioncontext__')


# Private hack
def dynamic_get(longvarname):
    import sys
    f = sys._getframe()
    while f:
        if f.f_locals.has_key(var):
            return f.f_locals[var]
        f = f.f_back
    raise NameError, "or something"
            
