from interpreter.baseobjspace import *
from multimethod import *


##################################################################

class StdObjSpace(ObjSpace):
    """The standard object space, implementing a general-purpose object
    library in Restricted Python."""

    def initialize(self):
        pass

    def wrap(self, x):
        "Wraps the Python value 'x' into one of the wrapper classes."
        if isinstance(x, int):
            import intobject
            return intobject.W_IntObject(x)
        if isinstance(x, str):
            import stringobject
            return stringobject.W_StringObject(x)
        if isinstance(x, float):
            import floatobject
            return floatobject.W_FloatObject(x)
        raise TypeError, "don't know how to wrap instances of %s" % type(x)

    def newtuple(self, list_w):
        import tupleobject
        return tupleobject.W_TupleObject(list_w)

    def newlist(self, list_w):
        import listobject
        return listobject.W_ListObject(list_w)

    def newdict(self, list_pairs_w):
        import dictobject
        return dictobject.W_DictObject(list_pairs_w)

    def newslice(self, w_start, w_end, w_step):
        # w_step may be a real None
        import sliceobject
        return sliceobject.W_SliceObject(w_start, w_end, w_step)

    def newfunction(self, w_code, w_globals, w_defaultarguments, w_closure=None):
        import funcobject
        return funcobject.W_FuncObject(w_code, w_globals,
                                       w_defaultarguments, w_closure)

    # special multimethods
    unwrap = MultiMethod('unwrap', 1)    # returns an unwrapped value
    compare = MultiMethod('compare', 2)  # extra 3rd arg is a Python string


# add all regular multimethods to StdObjSpace
for _name, _symbol, _arity in ObjSpace.MethodTable:
    setattr(StdObjSpace, _name, MultiMethod(_arity, _symbol))
