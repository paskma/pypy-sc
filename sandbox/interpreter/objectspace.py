

class ObjectSpace:

    def __init__(self):
        self.w_builtins = self.newdict([])
        self.w_modules  = self.newdict([])

    def initialize(self, executioncontext):
        "Abstract method to be overridden."
