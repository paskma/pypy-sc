from stdobjspace import StdObjSpace

class W_StringObject(object):
    __slots__ = ['value']
    def __init__(w_self, str):
        w_self.value = str
        
def getitem_str_int(space, w_str, w_int):
    return W_StringObject(w_str.value[w_int.intval])

StdObjectSpace.getitem.register(getitem_str_int, 
                                W_StringObject, W_IntObject)

def getitem_str_slice(space, w_str, w_slice):
    return applicationfile.call(space, "getitem_string_slice", [w_str, w_slice])

StdObjectSpace.getitem.register(getitem_str_slice, 
                                W_StringObject, W_SliceObject)
