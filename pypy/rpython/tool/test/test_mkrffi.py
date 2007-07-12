
import ctypes
from pypy.rpython.tool.mkrffi import *
from pypy.rpython.tool.test.test_c import TestBasic
import py

class random_structure(ctypes.Structure):
    _fields_ = [('one', ctypes.c_int),
                ('two', ctypes.POINTER(ctypes.c_int))]

def test_rffisource():
    res = RffiSource({1:2, 3:4}, "ab") + RffiSource(None, "c")
    assert res.structures == {1:2, 3:4}
    assert str(res.code) == "ab\nc"
    res += RffiSource({5:6})
    assert 5 in res.structures.keys()

def test_proc_tp_simple():
    rffi_source = RffiSource()
    assert rffi_source.proc_tp(ctypes.c_int) == 'rffi.INT'
    assert rffi_source.proc_tp(ctypes.c_void_p) == 'rffi.VOIDP'

def test_proc_tp_complicated():
    rffi_source = RffiSource()    
    assert rffi_source.proc_tp(ctypes.POINTER(ctypes.c_uint)) == \
           "lltype.Ptr(lltype.Array(rffi.UINT, hints={'nolength': True}))"
    rffi_source.proc_tp(random_structure)
    _src = py.code.Source("""
    c_random_structure = rffi.CStruct('random_structure', ('one', rffi.INT), ('two', lltype.Ptr(lltype.Array(rffi.INT, hints={'nolength': True}))))
    """)
    src = rffi_source.structures[random_structure]
    assert src.strip() == _src.strip(), str(src) + "\n" + str(_src)

class TestMkrffi(TestBasic):
    def test_single_func(self):
        func = self.lib.int_to_void_p
        func.argtypes = [ctypes.c_int]
        func.restype = ctypes.c_voidp

        src = RffiSource()
        src.proc_func(func)
        _src = py.code.Source("""
        c_int_to_void_p = rffi.llexternal('int_to_void_p', [rffi.INT], rffi.VOIDP)
        """)

        assert src.code == _src, str(src) + "\n" + str(_src)

    def test_struct_return(self):
        func = self.lib.int_int_to_struct_p
        func.argtypes = [ctypes.c_int, ctypes.c_int]
        func.restype = ctypes.POINTER(random_structure)
        rffi_source = RffiSource()
        rffi_source.proc_func(func)
        assert random_structure in rffi_source.structures
        _src = py.code.Source("""
        c_int_int_to_struct_p = rffi.llexternal('int_int_to_struct_p', [rffi.INT, rffi.INT], lltype.Ptr(c_random_structure))
        """)
        src = rffi_source.code
        assert src.strip() == _src.strip(), str(src) + "\n" + str(_src)