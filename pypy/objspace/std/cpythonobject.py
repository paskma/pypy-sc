

class W_CPythonObject:
    "Temporary class!  This one wraps *any* CPython object."

    delegate_once = {}
    
    def __init__(w_self, cpyobj):
        w_self.cpyobj = cpyobj

    def __repr__(w_self):
        """ representation for debugging purposes """
        return "wrap(%r)" % (w_self.cpyobj,)

