from objspace import *


class X:
    delegate_once = {}

def from_y_to_x(space, yinstance):
    x = X()
    print "from_y_to_x: %s -> %s" % (yinstance, x)
    return x

class Y:
    delegate_once = {X: from_y_to_x}



def add_x_x(space, x1, x2):
    print "add_x_x", space, x1, x2

def add_x_y(space, x1, y2):
    print "add_x_y", space, x1, y2

def add_y_y(space, y1, y2):
    raise FailedToImplement
    print "add_y_y", space, y1, y2

def add_string_string(space, x, y):
    print "add_string_string", space, x, y

def add_int_string(space, x, y):
    print "add_int_string", space, x, y

StdObjectSpace.add.register(add_x_x,           X,   X)
StdObjectSpace.add.register(add_x_y,           X,   Y)
StdObjectSpace.add.register(add_y_y,           Y,   Y)
StdObjectSpace.add.register(add_string_string, str, str)
StdObjectSpace.add.register(add_int_string,    int, str)


space = StdObjectSpace()
space.add(X(), X())
space.add(X(), Y())
space.add(Y(), X())
space.add(Y(), Y())
space.add(5,"test")
space.add("x","y")
space.add(3,4)
