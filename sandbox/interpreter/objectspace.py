import os
import executioncontext, pyframe


class OperationError(Exception):
    """Interpreter-level exception that signals an exception that should be
    sent to the application level.
    
    Arguments are the object-space exception class and value."""


class NoValue(Exception):
    """Raised to signal absence of value, e.g. in the iterator accessing
    method 'iternext()' of object spaces."""



class HelperBytecode:
    def __init__(self, source, filename='<helper>'):
        self.bytecode = compile(source, filename, 'exec')


class AppFile(HelperBytecode):
    """Dynamic loader of a set of Python functions and objects that
    should work at the application level (conventionally in .app.py files)"""

    # absolute name of the parent directory
    ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, filename):
        "Load and compile the file."
        # XXX looking for a pre-compiled file here will be quite essential
        #     when we want to bootstrap the compiler
        fullfn = os.path.join(AppFile.ROOTDIR, filename)
        f = open(fullfn, 'r')
        src = f.read()
        f.close()
        HelperBytecode.__init__(self, src, filename)


class Helper:

    def __init__(self, space, appfile):
        "Send the helper module to the given object space."
        self.space = space
        # initialize the module by running the bytecode in a new
        # dictionary, in a new execution context
        ec = executioncontext.ExecutionContext(space)
        self.w_namespace = ec.make_standard_w_globals()
        frame = pyframe.PyFrame(space, appfile.bytecode,
                                self.w_namespace, self.w_namespace)
        ec.eval_frame(frame)

    def get(self, objname):
        "Returns a wrapped copy of an object by name."
        w_name = space.wrap(objname)
        w_obj = space.getitem(self.w_namespace, w_name)
        return w_obj

    def call(self, functionname, argumentslist):
        w_function = self.get(space, functionname)
        w_arguments = space.newtuple(argumentslist)
        return space.apply(w_function, w_arguments)


##################################################################

class ObjectSpace:
    """Base class for the interpreter-level implementations of object spaces.
    XXX describe here in more details what the object spaces are."""

    def __init__(self):
        "Basic initialization of objects.  Override me."
        self.w_builtins = self.newdict([])
        self.w_modules  = self.newdict([])
        self.appfile_helpers = {}

    def getexecutioncontext(self):
        "Return what we consider to be the active execution context."
        import sys
        f = sys._getframe()           # !!hack!!
        while f:
            if f.f_locals.has_key('__executioncontext__'):
                result = f.f_locals['__executioncontext__']
                if result.space is self:
                    return result
            f = f.f_back
        raise ValueError, "no active execution context found"

    def gethelper(self, applicationfile):
        try:
            helper = self.appfile_helpers[applicationfile]
        except KeyError:
            helper = Helper(self, applicationfile)
            self.appfile_helpers[applicationfile] = helper
        return helper

    AppFile = AppFile   # make that class available for convenience
