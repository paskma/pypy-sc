print 'test right objspace'

class FailedToImplement(Exception):
    def __init__(self,e):
        self.e = e

class FakeRegister:
    def register(self,*argl,**argv):
        pass

class CallWrapper:
    def __init__(self,calldict):
        self._calldict = calldict

    def call(self,space,methodname,attributes):
        return self._calldict[methodname](*attributes)

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

    w_TypeError = "w_TypeError"
    w_OverflowError = "w_OverflowError"

    def wrap(self,item):
        return item

    def unwrap(self,item):
        return item

    def applicationfile(self,name):
        thisglobals = {}
        thislocals = {}
        execfile(name+'-app.py',thisglobals,thislocals)
        ret = CallWrapper(thislocals)
        return ret

StdObjSpace = ObjSpace()

if __name__ == '__main__':
    space = StdObjSpace()
    handle = space.applicationfile('test')
    handle.call(space,'test',[2])
