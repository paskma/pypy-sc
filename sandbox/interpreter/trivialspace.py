#
# Trivial object space for testing
# Does not perform any wrapping and (more importantly) does not
# correctly wrap the exceptions.
#

import pypy, operator, types, new

# The module itself is the object space; no TrivialSpace class here.


# general stuff
def wrap(x):
    return x

def unwrap(w):
    return w

# from the built-ins
type      = type
#no used yet: checktype = isinstance  # no tuple of types is allowed in 'checktype'
apply     = apply
newtuple  = tuple
newlist   = list
newdict   = dict
newslice  = slice  # maybe moved away to application-space at some time
getiter   = iter
repr      = repr
pow       = pow
getattr   = getattr
setattr   = setattr
delattr   = delattr
is_true   = operator.truth
# 'is_true' is not called 'truth' because it returns a *non-wrapped* boolean

# operators (!! no exception wrapping !!)
from operator import pos, neg, not_, invert
from operator import mul, truediv, floordiv, div, mod
from operator import add, sub, lshift, rshift, and_, xor, or_
from operator import getitem, setitem, delitem

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
    # from PyErr_GivenExceptionMatches
    if isinstance(w2, tuple):
        for exc in w2:
            if exc_match(w1, exc):
                return True
        return False
    if isinstance(w1, types.InstanceType):
        w1 = w1.__class__
    if isinstance(w1, types.ClassType) and isinstance(w2, types.ClassType):
        return issubclass(w1, w2)
    return w1 is w2

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
