from objspace import StdObjSpace
from pypy import AppFile
from intobject import W_IntObject

applicationfile = AppFile("stringobject.app.py")

class W_StringObject(object):
    __slots__ = ['value']
    def __init__(w_self, str):
        w_self.value = str
    def nonzero(w_self):
        return W_IntObject(w_self.value != 0)
    def hash(w_self):
        return W_IntObject(hash(self.value))
    

def getitem_str_int(space, w_str, w_int):
    return W_StringObject(w_str.value[w_int.intval])

StdObjectSpace.getitem.register(getitem_str_int, 
                                W_StringObject, W_IntObject)

def getitem_str_slice(space, w_str, w_slice):
    return applicationfile.call(space, "getitem_string_slice", [w_str, w_slice])

StdObjectSpace.getitem.register(getitem_str_slice, 
                                W_StringObject, W_SliceObject)

def add_str_str(space, w_left, w_right):
    return W_StringObject(w_left.value + w_right.value)

StdObjectSpace.getitem.register(add_str_str, W_StringObject, W_StringObject)

def mod_str_ANY(space, w_left, w_right):
    notImplemented
 
def mod_str_tuple(space, w_format, w_args):
    notImplemented


