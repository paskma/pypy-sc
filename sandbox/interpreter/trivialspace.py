#
# Trivial object space for testing
# Does not perform any wrapping and (more importantly) does not
# correctly wrap the exceptions.
#

import pypy, pyframe
import operator, types, new, sys

# The module itself is the object space; no TrivialSpace class here.


# general stuff
def wrap(x):
    return x

def unwrap(w):
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

def getattr(w_obj, w_name):
    try:
        obj = unwrap(w_obj)
        name = unwrap(w_name)
        return __builtins__.getattr(obj, name)
    except:
        raise pypy.OperationError(*sys.exc_info()[:2])
    
for _name in ('pos', 'neg', 'not_', 'pos', 'neg', 'not_', 'invert',
             'mul', 'truediv', 'floordiv', 'div', 'mod',
             'add', 'sub', 'lshift', 'rshift', 'and_', 'xor', 'or_',
             'getitem', 'setitem', 'delitem'):
    exec """
def %(_name)s(*args):
    try:
        return operator.%(_name)s(*args)
    except:
        cls, value, tb = sys.exc_info()
        raise pypy.OperationError(cls, value)
""" % locals()

# in-place operators
def inplace_pow(w1, w2):
    w1 **= w2
    return w1
def inplace_mul(w1, w2):
    w1 *= w2
    return w1
def inplace_truediv(w1, w2):
    w1 /= w2  # XXX depends on compiler flags
    return w1
def inplace_floordiv(w1, w2):
    w1 //= w2
    return w1
def inplace_div(w1, w2):
    w1 /= w2  # XXX depends on compiler flags
    return w1
def inplace_mod(w1, w2):
    w1 %= w2
    return w1

def inplace_add(w1, w2):
    w1 += w2
    return w1
def inplace_sub(w1, w2):
    w1 -= w2
    return w1
def inplace_lshift(w1, w2):
    w1 <<= w2
    return w1
def inplace_rshift(w1, w2):
    w1 >>= w2
    return w1
def inplace_and(w1, w2):
    w1 &= w2
    return w1
def inplace_or(w1, w2):
    w1 |= w2
    return w1
def inplace_xor(w1, w2):
    w1 ^= w2
    return w1


# misc
def iternext(w):
    try:
        return w.next()
    except StopIteration:
        raise pypy.NoValue

def newfunction(code, globals, defaultarguments, closure=None):
    return new.function(code, globals, None, defaultarguments, closure)

def apply(callable, args, kwds):
    if isinstance(callable, types.FunctionType):
        import trivialspace as space
        import executioncontext
        bytecode = callable.func_code
        w_globals = space.wrap(callable.func_globals)
        w_locals = space.newdict([])
        frame = pyframe.PyFrame(space, bytecode, w_globals, w_locals)
        # perform call
        frame.setargs(args, kwds)
        ec = executioncontext.getexecutioncontext()
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

def richcompare(w1, w2, operation):
    fn = operation_by_name[operation]
    return fn(w1, w2)
