from objspace import *

applicationfile = StdObjSpace.applicationfile(__name__)

class W_IntObject:

    delegate_once = {}
    
    def __init__(w_self, intval):
        w_self.intval = intval

    def getattr(w_self, space, w_attrname):
        #w_class = space.wrap("__class__")
    #w_result = space.richcompare(w_attrname, w_class, "==")
        #if space.is_true(w_result):
        #    return w_inttype
        #return applicationfile.call(space, "int_getattr", [w_self, w_attrname])

"""
XXX not implemented:
free list
FromLong
AsLong
FromString
FromUnicode
print
"""

def int_repr(space, w_int1):
    a = w_int1.intval
    res = "%ld" % a
    return space.wrap(a)

def int_compare(space, w_int1, w_int2):
    i = w_int1.intval
    j = w_int2.intval
    if i < j:
        ret = -1
    elif i > j:
        ret = 1
    else:
        ret = 0
    return W_IntObject(ret)

StdObjSpace.compare.register(int_int_compare, W_IntObject, W_IntObject)

def int_hash(w_int1):
    #/* XXX If this is changed, you also need to change the way
    #   Python's long, float and complex types are hashed. */
    x = w_int1.intval
    if x == -1:
        x = -2
    return W_IntObject(x)

StdObjSpace.hash.register(int_int_hash, W_IntObject, W_IntObject)

def int_int_add(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x + y
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer addition"))
    return W_IntObject(z)

StdObjSpace.add.register(int_int_add, W_IntObject, W_IntObject)

def int_int_sub(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x - y
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer substraction"))
    return W_IntObject(z)

StdObjSpace.sub.register(int_int_sub, W_IntObject, W_IntObject)

def int_int_mul(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x * y
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer multiplication"))
    return W_IntObject(z)

StdObjSpace.mul.register(int_int_mul, W_IntObject, W_IntObject)

def int_int_floordiv(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x // y
    except ZeroDivisionError:
        raise OperationError(space.w_ZeroDivisionError,
                             space.wrap("integer division by zero"))
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer division"))
    return W_IntObject(z)

StdObjSpace.floordiv.register(int_int_floordiv, W_IntObject, W_IntObject)

def int_int_truediv(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x / y   # XXX make sure this is the new true division
    except ZeroDivisionError:
        raise OperationError(space.w_ZeroDivisionError,
                             space.wrap("integer division by zero"))
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer division"))
    return W_IntObject(z)

StdObjSpace.truediv.register(int_int_truediv, W_IntObject, W_IntObject)

def int_int_mod(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x % y
    except ZeroDivisionError:
        raise OperationError(space.w_ZeroDivisionError,
                             space.wrap("integer modulo by zero"))
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer modulo"))
    return W_IntObject(z)

StdObjSpace.mod.register(int_int_mod, W_IntObject, W_IntObject)

def int_int_divmod(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x // y
    except ZeroDivisionError:
        raise OperationError(space.w_ZeroDivisionError,
                             space.wrap("integer divmod by zero"))
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer modulo"))
    # no overflow possible
    m = x % y
    return space.newtuple([W_IntObject(z), W_IntObject(m)])

StdObjSpace.divmod.register(int_int_divmod, W_IntObject, W_IntObject)

## install the proper int_int_div
if 1 / 2 == 1 // 2:
    int_int_div = int_int_floordiv
else:
    int_int_div = int_int_truediv

StdObjSpace.div.register(int_int_div, W_IntObject, W_IntObject)

# helper for pow()

def _impl_int_int_pow(iv, iw, iz=None):
    if iw < 0:
        if iz is not None:
            raise OperationError(space.w_TypeError,
                             space.wrap("pow() 2nd argument "
                 "cannot be negative when 3rd argument specified"))
        #/* Return a float.  This works because we know that
        #   this calls float_pow() which converts its
        #   arguments to double. */
        ## actually bounce it
        raise FailedToImplement(space.w_ValueError,
                                space.wrap("integer exponentiation"))
    if iz is not None:
        if iz == 0:
            raise FailedToImplement(space.w_ValueError,
                                    space.wrap("pow() 3rd argument cannot be 0"))
    temp = iv
    ix = 1
    while iw > 0:
        if iw & 1 {
            try:
                ix = ix*temp
            except OverflowError:
                raise FailedToImplement(space.w_OverflowError,
                                        space.wrap("integer exponentiation"))
        iw >>= 1   #/* Shift exponent down by 1 bit */
        if iw==0:
            break
        try:
            temp *= temp   #/* Square the value of temp */
        except OverflowError:
            raise FailedToImplement(space.w_OverflowError,
                                    space.wrap("integer exponentiation"))
        if iz:
            #/* If we did a multiplication, perform a modulo */
            try:
                ix = ix % iz;
                temp = temp % iz;
            except OverflowError:
                raise FailedToImplement(space.w_OverflowError,
                                        space.wrap("integer exponentiation"))
    if iz:
        try:
            ix = ix % iz
        except OverflowError:
            raise FailedToImplement(space.w_OverflowError,
                                    space.wrap("integer exponentiation"))
    return W_IntObject(ix)

def int_int_int_pow(space, w_int1, w_int2, w_int3):
    x = w_int1.intval
    y = w_int2.intval
    z = w_int3.intval
    ret = _impl_int_int_pow(x, y, z)
    return W_IntObject(ret)

StdObjSpace.pow.register(int_int_int_pow, W_IntObject, W_IntObject, W_IntObject)

def int_int_none_pow(space, w_int1, w_int2, w_none):
    x = w_int1.intval
    y = w_int2.intval
    ret = _impl_int_int_pow(x, y)
    return W_IntObject(ret)

StdObjSpace.pow.register(int_int_none_pow, W_IntObject, W_IntObject, W_NoneObject)

def int_neg(space, w_int1):
    a = w_int1.intval
    try:
        x = -a
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer negation"))
    return W_IntObject(x)

StdObjSpace.neg.register(int_neg, W_IntObject)

# int_pos is supposed to do nothing, unless it has
# a derived integer object, where it should return
# an exact one.
def int_pos(space, w_int1):
    #not sure if this should be done this way:
    if w_int1.__class__ is W_IntObject:
        return w_int1
    a = w_int1.intval
    return W_IntObject(a)

StdObjSpace.pos.register(space, int_pos, W_IntObject)

def int_abs(space, w_int1):
    if w_int1.intval >= 0:
        return int_pos(space, w_int1)
    else
        return int_neg(space, w_int1)

StdObjSpace.abs.register(int_abs, W_IntObject)

# this is just an internal test, used where?
def int_nonzero(space, w_int1):
    return w_int1->intval != 0

def int_invert(space, w_int1):
    x = w_int1.intval
    a = ~ x
    return W_IntObject(a)

StdObjSpace.invert.register(int_invert, W_IntObject)

# belongs to pyconfig.h
LONG_BIT = 32  # XXX put this elsewhere and make it machine dependant

WARN_SHIFT = type(1 << LONG_BIT) == int

# helper for warning
# it either does nothing since warning must be implemented,
# 

def _warn_or_raise_lshift():
    if WARN_SHIFT:
        pass  # dunno how to warn
        #if (PyErr_Warn(PyExc_FutureWarning,
        #           "x<<y losing bits or changing sign "
        #           "will return a long in Python 2.4 and up") < 0)
    else:
        # we want to coerce to long
        raise FailedToImplement(space.w_OverflowError,
                                space.wrap("integer left shift"))
        
def int_int_lshift(space, w_int1, w_int2):
    a = w_int1.intval
    b = w_int2.intval
    if b < 0:
        raise OperationError(space.w_ValueError,
                             space.wrap("negative shift count"))
    if a == 0 or b == 0:
        return int_pos(w_int1)
    if b >= LONG_BIT:
        _warn_or_raise_lshift()
        return W_IntObject(0)
    ##
    ## XXX please! have a look into pyport.h and see how to implement
    ## the overflow checking, using macro Py_ARITHMETIC_RIGHT_SHIFT
    ## we *assume* that the overflow checking is done correctly
    ## in the code generator, which is not trivial!
    try:
        c = a << b
        ## the test in C code is
        ## if (a != Py_ARITHMETIC_RIGHT_SHIFT(long, c, b)) {
        ##     if (PyErr_Warn(PyExc_FutureWarning,
        # and so on
    except OverflowError:
        _warn_or_raise_lshift()
        return W_IntObject(0)
    return W_IntObject(c);

StdObjSpace.lshift.register(int_int_lshift, W_IntObject, W_IntObject)

def int_int_rshift(space, w_int1, w_int2):
    a = w_int1.intval
    b = w_int2.intval
    if b < 0:
        raise OperationError(space.w_ValueError,
                             space.wrap("negative shift count"))
    if a == 0 or b == 0:
        return int_pos(v)
    if b >= LONG_BIT:
        if a < 0:
            a = -1
        else:
            a = 0
    else:
        ## look into pyport.h, who >> should be implemented!
        ## a = Py_ARITHMETIC_RIGHT_SHIFT(long, a, b);
        a = a >> b
    return W_IntObject(a)

StdObjSpace.lshift.register(int_int_rshift, W_IntObject, W_IntObject)

def int_int_and(space, w_int1, w_int2):
    a = w_int1.intval
    b = w_int2.intval
    res = a & b
    return W_IntObject(res)

StdObjSpace.and.register(int_int_and, W_IntObject, W_IntObject)

def int_int_xor(space, w_int1, w_int2):
    a = w_int1.intval
    b = w_int2.intval
    res = a ^ b
    return W_IntObject(res)

StdObjSpace.xor.register(int_int_xor, W_IntObject, W_IntObject)

def int_int_or(space, w_int1, w_int2):
    a = w_int1.intval
    b = w_int2.intval
    res = a | b
    return W_IntObject(res)

StdObjSpace.or_.register(int_int_or, W_IntObject, W_IntObject)

# coerce is not wanted
##
##static int
##int_coerce(PyObject **pv, PyObject **pw)
##{
##    if (PyInt_Check(*pw)) {
##        Py_INCREF(*pv);
##        Py_INCREF(*pw);
##        return 0;
##    }
##    return 1; /* Can't do it */
##}

def int_int(space, w_int1):
    return w_int1

StdObjSpace.int.register(int_int, W_IntObject)

def int_long(space, w_int1):
    a = w_int1.intval
    return space.newlong(a)

StdObjSpace.long.register(int_long, W_IntObject)

def int_float(space, w_int1):
    a = w_int1.intval
    x = float(a)
    return space.newdouble(x)

StdObjSpace.float.register(int_float, W_IntObject)

def int_oct(space.w_int1):
    x = w_int1.intval
    if x < 0:
        ## XXX what about this warning?
        #if (PyErr_Warn(PyExc_FutureWarning,
        #           "hex()/oct() of negative int will return "
        #           "a signed string in Python 2.4 and up") < 0)
        #    return NULL;
        pass
    if x == 0:
        ret = "0"
    else:
        ret = "0%lo" % x
    return space.wrap(ret)

StdObjSpace.oct.register(int_oct, W_IntObject)

def int_hex(space.w_int1):
    x = w_int1.intval
    if x < 0:
        ## XXX what about this warning?
        #if (PyErr_Warn(PyExc_FutureWarning,
        #           "hex()/oct() of negative int will return "
        #           "a signed string in Python 2.4 and up") < 0)
        #    return NULL;
        pass
    if x == 0:
        ret = "0"
    else:
        ret = "0x%lx" % x
    return space.wrap(ret)

StdObjSpace.hex.register(int_hex, W_IntObject)
