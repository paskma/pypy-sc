import sys,os
import pyframe


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
        "Load and compile the file."
        # XXX looking for a pre-compiled file here will be quite essential
        #     when we want to bootstrap the compiler
        
        # XXX path handling is just done in a dummy way for now
        fullfn = os.path.join(os.path.dirname(__file__), filename)
        f = open(fullfn, 'r')
        src = f.read()
        f.close()
        self.bytecode = compile(src, filename, 'exec')

    def sendto(self, space):
        """Send the module to the given object space.
        This is done only once; we maintain a cache in the space object."""
        try:
            cache = space.__appfilecache__
        except AttributeError:
            cache = space.__appfilecache__ = {}
        try:
            w_namespace = cache[self]
        except KeyError:
            # initialize the module by running the bytecode in a new
            # dictionary
            w_namespace = cache[self] = space.newdict([])
            frame = pyframe.PyFrame(space, self.bytecode,
                                    w_namespace, w_namespace)
            frame.eval()
        return w_namespace

    def findobject(self, space, name):
        "Returns a wrapped copy of an object by name."
        w_namespace = self.sendto(space)
        w_name = space.wrap(name)
        w_obj = space.getitem(w_namespace, w_name)
        return w_obj

    def call(self, space, functionname, argumentslist):
        w_function = self.findobject(space, functionname)
        w_arguments = space.newtuple(argumentslist)
        return space.apply(w_function, w_arguments)
