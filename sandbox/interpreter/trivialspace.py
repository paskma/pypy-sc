#
# Trivial object space for testing
# Does not perform any wrapping and (more importantly) does not
# correctly wrap the exceptions.
#

import pyframe, objectspace
import operator, types, new, sys

class TrivialSpace(objectspace.ObjectSpace):

    def initialize(self):
        import __builtin__, types
        self.w_builtins.update(__builtin__.__dict__)
        for n, c in self.w_builtins.iteritems():
            if isinstance(c, types.ClassType) and issubclass(c, Exception):
                setattr(self, 'w_' + c.__name__, c)
        self.w_None = None
        self.w_True = True
        self.w_False = False

    # general stuff
    def wrap(self, x):
        return x

    def unwrap(self, w):
        return w

    # from the built-ins
    type      = type
    #no used yet: checktype = isinstance  # no tuple of types is allowed in 'checktype'
    newtuple  = tuple
    newlist   = list
    newdict   = dict
    newslice  = slice  # maybe moved away to application-space at some time
    getiter   = iter
    repr      = repr
    pow       = pow
    setattr   = setattr
    delattr   = delattr
    is_true   = operator.truth
    # 'is_true' is not called 'truth' because it returns a *non-wrapped* boolean

    def getattr(self, w_obj, w_name):
        try:
            obj = unwrap(w_obj)
            name = unwrap(w_name)
            return __builtins__.getattr(obj, name)
        except:
            raise objectspace.OperationError(*sys.exc_info()[:2])

    for _name in ('pos', 'neg', 'not_', 'pos', 'neg', 'not_', 'invert',
                 'mul', 'truediv', 'floordiv', 'div', 'mod',
                 'add', 'sub', 'lshift', 'rshift', 'and_', 'xor', 'or_',
                 'getitem', 'setitem', 'delitem'):
        exec """
def %(_name)s(self, *args):
    try:
        return operator.%(_name)s(*args)
    except:
        cls, value, tb = sys.exc_info()
        raise objectspace.OperationError(cls, value)
""" % locals()

    # in-place operators
    def inplace_pow(self, w1, w2):
        w1 **= w2
        return w1
    def inplace_mul(self, w1, w2):
        w1 *= w2
        return w1
    def inplace_truediv(self, w1, w2):
        w1 /= w2  # XXX depends on compiler flags
        return w1
    def inplace_floordiv(self, w1, w2):
        w1 //= w2
        return w1
    def inplace_div(self, w1, w2):
        w1 /= w2  # XXX depends on compiler flags
        return w1
    def inplace_mod(self, w1, w2):
        w1 %= w2
        return w1

    def inplace_add(self, w1, w2):
        w1 += w2
        return w1
    def inplace_sub(self, w1, w2):
        w1 -= w2
        return w1
    def inplace_lshift(self, w1, w2):
        w1 <<= w2
        return w1
    def inplace_rshift(self, w1, w2):
        w1 >>= w2
        return w1
    def inplace_and(self, w1, w2):
        w1 &= w2
        return w1
    def inplace_or(self, w1, w2):
        w1 |= w2
        return w1
    def inplace_xor(self, w1, w2):
        w1 ^= w2
        return w1


    # misc
    def iternext(self, w):
        try:
            return w.next()
        except StopIteration:
            raise objectspace.NoValue

    def newfunction(self, code, globals, defaultarguments, closure=None):
        if closure is None:   # temp hack
            return new.function(code, globals, None, defaultarguments)
        return new.function(code, globals, None, defaultarguments, closure)

    def newstring(self, asciilist):
        return ''.join([chr(ascii) for ascii in asciilist])

    def apply(self, callable, args, kwds):
        if isinstance(callable, types.FunctionType):
            bytecode = callable.func_code
            ec = self.getexecutioncontext()
            w_globals = self.wrap(callable.func_globals)
            w_locals = self.newdict([])
            frame = pyframe.PyFrame(self, bytecode, w_globals, w_locals)
            # perform call
            frame.setargs(args, kwds)
            return ec.eval_frame(frame)
        else:
            return __builtins__.apply(callable, args, kwds)

    # comparisons
    def in_(w1, w2):
        return w1 in w2

    def not_in(w1, w2):
        return w1 not in w2

    def is_(w1, w2):
        return w1 is w2

    def is_not(w1, w2):
        return w1 is not w2

    def exc_match(w1, w2):
        try:
            try:
                raise w1
            except w2:
                return True
        except:
            return False

    operation_by_name = {
        '<':  operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>':  operator.gt,
        '>=': operator.ge,
        'in': in_,
        'not in': not_in,
        'is': is_,
        'is not': is_not,
        'exc match': exc_match,
        }

    def richcompare(self, w1, w2, operation):
        fn = self.operation_by_name[operation]
        return fn(w1, w2)
