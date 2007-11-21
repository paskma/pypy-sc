
from pypy.interpreter.typedef import TypeDef, GetSetProperty
from pypy.interpreter.baseobjspace import W_Root, ObjSpace, Wrappable, \
     Arguments
from pypy.interpreter.gateway import interp2app
from pypy.interpreter.error import OperationError
from pypy.interpreter.callmethod import object_getattribute
from pypy.interpreter.function import StaticMethod, Method

class W_Super(Wrappable):
    def __init__(self, space, w_selftype, w_starttype, w_type, w_self):
        self.w_selftype = w_selftype
        self.w_starttype = w_starttype
        self.w_type = w_type
        self.w_self = w_self

    def get(self, space, w_obj, w_type=None):
        w = space.wrap
        if self.w_self is None or space.is_w(w_obj, space.w_None):
            return w(self)
        else:
            return space.call_function(self.w_selftype, self.w_starttype, w_obj
                                       )
    get.unwrap_spec = ['self', ObjSpace, W_Root, W_Root]

    def getattribute(self, space, name):
        w = space.wrap
        if name == '__class__':
            return self.w_selftype
        if self.w_type is None:
            return space.call_function(object_getattribute(space),
                                       w(self), w(name))
            
        w_value = space.lookup_in_type_starting_at(self.w_type,
                                                   self.w_starttype,
                                                   name)
        if w_value is None:
            return space.getattr(w(self), w(name))

        try:
            w_get = space.getattr(w_value, space.wrap('__get__'))
            if space.is_w(self.w_self, self.w_type):
                w_self = space.w_None
            else:
                w_self = self.w_self
        except OperationError, o:
            if not o.match(space, space.w_AttributeError):
                raise
            return w_value
        return space.call_function(w_get, w_self, self.w_type)
    getattribute.unwrap_spec = ['self', ObjSpace, str]

def descr_new_super(space, w_self, w_starttype, w_obj_or_type=None):
    if space.is_w(w_obj_or_type, space.w_None):
        w_type = None  # unbound super object
    else:
        w_objtype = space.type(w_obj_or_type)
        if space.is_true(space.issubtype(w_objtype, space.w_type)) and \
            space.is_true(space.issubtype(w_obj_or_type, w_starttype)):
            w_type = w_obj_or_type # special case for class methods
        elif space.is_true(space.issubtype(w_objtype, w_starttype)):
            w_type = w_objtype # normal case
        else:
            try:
                w_type = space.getattr(w_obj_or_type, space.wrap('__class__'))
            except OperationError, o:
                if not o.match(space, space.w_AttributeError):
                    raise
                w_type = w_objtype
            if not space.is_true(space.issubtype(w_type, w_starttype)):
                raise OperationError(space.w_TypeError,
                    space.wrap("super(type, obj): "
                               "obj must be an instance or subtype of type"))
    return space.wrap(W_Super(space, w_self, w_starttype, w_type, w_obj_or_type))
descr_new_super.unwrap_spec = [ObjSpace, W_Root, W_Root, W_Root]

W_Super.typedef = TypeDef(
    'super',
    __new__          = interp2app(descr_new_super),
    __getattribute__ = interp2app(W_Super.getattribute),
    __get__          = interp2app(W_Super.get),
    __doc__          =     """super(type) -> unbound super object
super(type, obj) -> bound super object; requires isinstance(obj, type)
super(type, type2) -> bound super object; requires issubclass(type2, type)

Typical use to call a cooperative superclass method:

class C(B):
    def meth(self, arg):
        super(C, self).meth(arg)"""
)

class W_ClassMethod(Wrappable):
    def __init__(self, w_function):
        self.w_function = w_function

    def new(space, w_type, w_function):
        if not space.is_true(space.callable(w_function)):
            name = space.getattr(space.type(w_function), space.wrap('__name__'))
            raise OperationError(space.w_TypeError, space.wrap(
                                 "'%s' object is not callable" % name))
        return W_ClassMethod(w_function)

    def get(self, space, w_obj, w_klass=None):
        if space.is_w(w_klass, space.w_None):
            w_klass = space.type(w_obj)
        return space.wrap(Method(space, self.w_function, w_klass, space.w_None))

W_ClassMethod.typedef = TypeDef(
    'classmethod',
    __new__ = interp2app(W_ClassMethod.new.im_func,
                         unwrap_spec=[ObjSpace, W_Root, W_Root]),
    __get__ = interp2app(W_ClassMethod.get,
                         unwrap_spec=['self', ObjSpace, W_Root, W_Root]),
    __doc__ = """classmethod(function) -> class method

Convert a function to be a class method.

A class method receives the class as implicit first argument,
just like an instance method receives the instance.
To declare a class method, use this idiom:

  class C:
      def f(cls, arg1, arg2, ...): ...
      f = classmethod(f)

It can be called either on the class (e.g. C.f()) or on an instance
(e.g. C().f()).  The instance is ignored except for its class.
If a class method is called for a derived class, the derived class
object is passed as the implied first argument.""",
)