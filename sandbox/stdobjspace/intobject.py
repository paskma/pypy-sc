from objspace import *



class W_IntObject:
    
    def __init__(w_self, intval):
        w_self.intval = intval

    def getattr(w_self, space, w_attrname):
        #w_class = space.wrap("__class__")
        #w_result = space.richcompare(w_attrname, w_class, "==")
        #if space.is_true(w_result):
        #    return w_inttype
        return applicationfile.call(space, "int_getattr", [w_self, w_attrname])





def int_add(space, w_int1, w_int2):
    x = w_int1.intval
    y = w_int2.intval
    try:
        z = x + y
    except OverflowError:
        raise FailedToImplement(OverflowError, "integer addition")
    return W_IntObject(z)

StdObjSpace.add.register(int_add, W_IntObject, w_IntObject)

