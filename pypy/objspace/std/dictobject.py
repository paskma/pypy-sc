from objspace import *
from stringobject import W_StringObject


class W_DictObject:
    delegate_once = {}

    def __init__(self, list_pairs_w):
        self.data = list_pairs_w


def getitem_dict_str(space, w_dict, w_lookup):
    # actually works with any key, but W_ANY is not implemented now
    data = w_dict.data
    for w_key, w_value in data:
        if space.is_true(space.compare(w_lookup, w_key, '==')):
            return w_value
    raise OperationError(space.w_KeyError, w_lookup)

StdObjSpace.getitem.register(getitem_dict_str, W_DictObject, W_StringObject)
