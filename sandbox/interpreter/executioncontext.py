import sys


class ExecutionContext:

    def __init__(self, space, w_builtins):
        self.space = space
        self.w_builtins = w_builtins
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
    ...
