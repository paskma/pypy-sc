
class W_TupleObject(object):
    def __init__(self, items):
        self.items = items   # a list of wrapped values


def tuple_unwrap(space, w_tuple):
    list_w_items = w_tuple.items
    items = [space.unwrap(w_item) for w_item in list_w_items]
    return tuple(items)

StdObjSpace.unwrap.register(tuple_unwrap, W_TupleObject)
