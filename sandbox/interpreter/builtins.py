import objectspace

appfile = objectspace.AppFile("interpreter/builtins.app.py")



def r_chr(space, w_ascii):
    w_character = space.newstring([w_ascii])
    return w_character


def init(space):
    builtins = objectspace.Module(space)
    #builtins.   ///.
    builtins.loadappfile(appfile)
