import new

class FailedToImplement(Exception):
    pass

class FakeRegister:
    def register(self,*argl,**argv):
        pass

class CallWrapper:
    def __init__(self,module):
        self._module = module

    def call(self,space,methodname,attributes):
        return getattr(self._module,methodname)(*attributes)
class W_NoneObject:pass

class ObjSpace:
    add = FakeRegister()
    sub = FakeRegister()
    mul = FakeRegister()
    pow = FakeRegister()
    pos = FakeRegister()
    neg = FakeRegister()
    not_ = FakeRegister()
    invert = FakeRegister()
    truediv = FakeRegister()
    floordiv = FakeRegister()
    div = FakeRegister()
    mod = FakeRegister()
    lshift = FakeRegister()
    rshift = FakeRegister()
    and_ = FakeRegister()
    xor = FakeRegister()
    or_ = FakeRegister()
    oct = FakeRegister()
    hex = FakeRegister()
    ord = FakeRegister()
    float = FakeRegister()
    repr = FakeRegister()
    str = FakeRegister()
    cmp = FakeRegister()
    hash = FakeRegister()
    divmod = FakeRegister()
    abs = FakeRegister()
    nonzero = FakeRegister()
    coerce = FakeRegister()
    int = FakeRegister()
    long = FakeRegister()
    float = FakeRegister()

    w_TypeError = "w_TypeError"
    w_OverflowError = "w_OverflowError"
    w_ZeroDivisionError = "w_ZeroDivisionError"

    def wrap(self,item):
        return item

    def unwrap(self,item):
        return item

    def AppFile(self,name):
        thismod = new.module(name+'_app')
        thisglobals = {}
        thislocals = {}
        try:
            execfile(name+'-app.py',thismod.__dict__)
        except IOError:
            execfile(name+'.app.py',thismod.__dict__)
        #namespace = thislocals.update(thisglobals)
        ret = CallWrapper(thismod)
        return ret

    def newtuple(self,tuplelist):
        return tuple(tuplelist)

    def newdouble(self,thisdouble):
        return thisdouble

StdObjSpace = ObjSpace()

if __name__ == '__main__':
    space = ObjSpace()
    handle = space.applicationfile('test')
    handle.call(space,'test',[2])
