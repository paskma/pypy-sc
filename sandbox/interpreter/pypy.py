import sys, operator


# use the operator module as the trivial, wrapping-less,
# exception-handling-less object space.
operator.wrap = operator.unwrap = lambda x: x
operator.type = type
trivialspace = operator


class OperationError(Exception):
    """Interpreter-level exception that signals an exception that should be
    sent to the application level.
    
    Arguments are the object-space exception class and value."""


class NoValue(Exception):
    """Raised to signal absence of value, e.g. in the iterator accessing
    method 'iternext()' of object spaces."""


class AppFile:
    """Dynamic loader of a set of Python functions and objects that
    should work at the application level (conventionally in .app.py files)"""

    def __init__(self, filename):
        pass #.....

    def findobject(self, space, name):
        pass #.....

    def call(self, space, functionname, argumentslist):
        w_function = self.findobject(space, functionname)
        w_arguments = space.new_tuple(argumentslist)
        return space.apply(w_function, w_arguments)
