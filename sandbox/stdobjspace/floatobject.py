from objspace import *



class W_FloatObject:
    
    def __init__(w_self, floatval):
        w_self.floatval = floatval

    def getattr(w_self, space, w_attrname):
        return applicationfile.call(space, "float_getattr", [w_self, w_attrname])


def w_float(space,w_value):
    return W_FloatObject(float(w_value))

def float_repr(space, w_float):
    ## %reimplement%
    # uses CPython "repr" builtin function
    return space.wrap(repr(w_float.floatvalue))

def float_str(space, w_float):
    ## %reimplement%
    # uses CPython "str" builtin function
    return space.wrap(str(w_float.floatvalue))

def float_float_compare(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    if x < y:
        return space.wrap(-1)
    elif x > y:
        return space.wrap(1)
    else:
        return space.wrap(0)
    
def float_hash(space,w_value):
    ## %reimplement%
    # real Implementation should be taken from _Py_HashDouble in object.c
    return space.wrap(hash(w_value.floatvalue)))

def float_float_add(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x + y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float addition"))
    return W_FloatObject(z)

def float_float_sub(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x - y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float substraction"))
    return W_FloatObject(z)

def float_float_mul(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x * y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float multiplication"))
    return W_FloatObject(z)

def float_float_div(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x / y   # XXX make sure this is the new true division
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float division"))
	# no overflow
    return W_FloatObject(z)

def float_float_rem(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
def float_float_pow(space, w_float1,w_float2,thirdArg=None):
    if thirdArg is not None:
        raise FailedToImplement(space.w_TypeError space.wrap("pow() 3rd argument not allowed unless all arguments are integers"))
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x ** y
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError, space.wrap("float power"))
    return W_FloatObject(z)


StdObjSpace.add.register(float_float_add, W_FloatObject, W_FloatObject)
StdObjSpace.sub.register(float_float_sub, W_FloatObject, W_FloatObject)
StdObjSpace.mul.register(float_float_mul, W_FloatObject, W_FloatObject)
StdObjSpace.div.register(float_float_div, W_FloatObject, W_FloatObject)
StdObjSpace.pow.register(float_float_pow, W_FloatObject, W_FloatObject)
