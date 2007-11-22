from pypy.rpython.lltypesystem.rffi import CConstant, CExternVariable
from pypy.rpython.lltypesystem import lltype, ll2ctypes

class CConstantErrno(CConstant):
    # these accessors are used when calling get_errno() or set_errno()
    # on top of CPython
    def __getitem__(self, index):
        assert index == 0
        try:
            return ll2ctypes.TLS.errno
        except AttributeError:
            raise ValueError("no C function call occurred so far, "
                             "errno is undefined")
    def __setitem__(self, index, value):
        assert index == 0
        ll2ctypes.TLS.errno = value

get_errno, set_errno = CExternVariable(lltype.Signed, 'errno', CConstantErrno,
                                       includes=['errno.h'], sandboxsafe=True)

