from objspace import *

applicationfile = StdObjSpace.applicationfile(__name__)

class W_FloatObject:
    
    def __init__(w_self, floatval):
        w_self.floatval = floatval

def float_float(space,w_value):
    if isinstance(w_value,W_FloatObject):
        return w_value
    else:
        return W_FloatObject(w_value.floatval)

StdObjSpace.float.register(float_float, W_FloatObject)

def float_repr(space, w_float):
    ## %reimplement%
    # uses CPython "repr" builtin function
    return space.wrap(repr(w_float.floatvalue))

StdObjSpace.repr.register(float_repr, W_FloatObject)

def float_str(space, w_float):
    ## %reimplement%
    # uses CPython "str" builtin function
    return space.wrap(str(w_float.floatvalue))

StdObjSpace.str.register(float_str, W_FloatObject)

def float_float_compare(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    if x < y:
        return space.wrap(-1)
    elif x > y:
        return space.wrap(1)
    else:
        return space.wrap(0)

StdObjSpace.cmp.register(float_float_compare, W_FloatObject, W_FloatObject)
    
def float_hash(space,w_value):
    ## %reimplement%
    # real Implementation should be taken from _Py_HashDouble in object.c
    return space.wrap(hash(w_value.floatvalue))

StdObjSpace.hash.register(float_hash, W_FloatObject)

def float_float_add(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x + y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float addition"))
    return W_FloatObject(z)

StdObjSpace.add.register(float_float_add, W_FloatObject, W_FloatObject)

def float_float_sub(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x - y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float substraction"))
    return W_FloatObject(z)

StdObjSpace.sub.register(float_float_sub, W_FloatObject, W_FloatObject)

def float_float_mul(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x * y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float multiplication"))
    return W_FloatObject(z)

StdObjSpace.mul.register(float_float_mul, W_FloatObject, W_FloatObject)

def float_float_div(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x / y   # XXX make sure this is the new true division
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float division"))
	# no overflow
    return W_FloatObject(z)

StdObjSpace.div.register(float_float_div, W_FloatObject, W_FloatObject)

def float_float_mod(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    if y == 0.0:
        raise FailedToImplement(space.w_ZeroDivisionError, space.wrap("float modulo"))
    try:
        # this is a hack!!!! must be replaced by a real fmod function
        mod = applicationfile.call(space, "float_fmod", [x,y])
        if (mod and ((y < 0.0) != (mod < 0.0))):
            mod += y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float division"))

    return W_FloatObject(mod)

StdObjSpace.mod.register(float_float_mod, W_FloatObject, W_FloatObject)

def float_float_divmod(space, w_float1, w_float2):
    x = w_float1.floatval
    y = w_float2.floatval
    if y == 0.0:
        raise FailedToImplement(space.w_ZeroDivisionError, space.wrap("float modulo"))
    try:
        # this is a hack!!!! must be replaced by a real fmod function
        mod = applicationfile.call(space, "float_fmod", [x,y])
        div = (x -mod) / y
        if (mod):
            if ((y < 0.0) != (mod < 0.0)):
                mod += y
                div -= -1.0
        else:
            mod *= mod
            if y < 0.0:
                mod = -mod
        if div:
            floordiv = applicationfile.call(space, "float_floor", [div])
            if (div - floordiv > 0.5):
                floordiv += 1.0
        else:
            div *= div;
            floordiv = div * x / y
    except FloatingPointError:
        raise FailedToImplement(space.w_FloatingPointError, space.wrap("float division"))

    return space.newtuple([floordiv,mod])

StdObjSpace.divmod.register(float_float_divmod, W_FloatObject, W_FloatObject)

def float_float_pow(space, w_float1,w_float2,thirdArg=None):
    if thirdArg is not None:
        raise FailedToImplement(space.w_TypeError,space.wrap("pow() 3rd argument not allowed unless all arguments are integers"))
    x = w_float1.floatval
    y = w_float2.floatval
    try:
        z = x ** y
    except OverflowError:
        raise FailedToImplement(space.w_OverflowError, space.wrap("float power"))
    return W_FloatObject(z)

StdObjSpace.pow.register(float_float_pow, W_FloatObject, W_FloatObject)
