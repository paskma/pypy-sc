from objspace import *



class W_IntObject:

    delegate_once = {}
    
    def __init__(w_self, intval):
        w_self.intval = intval

    def getattr(w_self, space, w_attrname):
        #w_class = space.wrap("__class__")
        #w_result = space.richcompare(w_attrname, w_class, "==")
        #if space.is_true(w_result):
        #    return w_inttype
        return applicationfile.call(space, "int_getattr", [w_self, w_attrname])


def int_int_add(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x + y
    except OverflowError:
        raise FailedToImplement(OverflowError, "integer addition")
    return W_IntObject(z)

def int_int_sub(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x - y
    except OverflowError:
        raise FailedToImplement(OverflowError, "integer subtraction")
    return W_IntObject(z)

def int_int_mul(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x * y
    except OverflowError:
        raise FailedToImplement(OverflowError, "integer multiplication")
    return W_IntObject(z)

def int_int_floordiv(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x // y
    except ZeroDivisionError:
		raise   # we have to implement the exception or it will be ignored
	# no overflow
    return W_IntObject(z)

def int_int_truediv(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x / y   # XXX make sure this is the new true division
    except ZeroDivisionError:
        raise OperationError(space.w_ZeroDivisionError,
                             space.wrap("integer division by zero"))
    # no overflow
    return W_IntObject(z)

def int_int_mod(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x % y
    except ZeroDivisionError:
		raise   # we have to implement the exception or it will be ignored
	# no overflow
    return W_IntObject(z)

def int_int_divmod(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
		z = x // y
		m = x % y
    except ZeroDivisionError:
		raise   # we have to implement the exception or it will be ignored
	# no overflow
    return W_TupleObject([z, m])



if 1 / 2 == 1 // 2:
	int_int_div = int_int_floordiv
else:
	int_int_div = int_int_truediv

StdObjSpace.add.register(int_add, W_IntObject, W_IntObject)
