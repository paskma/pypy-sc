
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
        return result


# Public
def getexecutioncontext():
    return dynamic_get('__executioncontext__')


# Private hack
def dynamic_get(longvarname):
    import sys
    f = sys._getframe()
    while f:
        if f.f_locals.has_key(longvarname):
            return f.f_locals[longvarname]
        f = f.f_back
    raise NameError, "or something"
