class StdObjectSpace:
    ...
    def wrap(self, x):
        ...
        if isinstance(x, int):
            return W_IntObject(x)
        ...


    def getattr(self, w_object, w_attrname):
        return w_object.getattr(self, w_attrname)
