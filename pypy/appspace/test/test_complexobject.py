#taken from CPython 2.3 (?)

import setpath
from pypy.appspace.complexobject import complex as pycomplex

import cmath
import math, sys, types, unittest

from support import *

def equal(a, b):
    "Compare two complex or normal numbers. 0 if different, 1 if roughly equal."
    
    numTypes = [types.IntType, types.LongType, types.FloatType]
    da, db = dir(a), dir(b)
    
    if 'real' in da and 'real' in db and 'imag' in da and 'imag' in db:
        if math.fabs(a.real-b.real) > 1e-10:
            return 0
        if math.fabs(a.imag-b.imag) > 1e-10:
            return 0
        else:
            return 1
    elif type(a) in numTypes and type(b) in numTypes:
        if math.fabs(a-b) > 1e-10:
            return 0
        else:
            return 1

def enumerate():
    valueRange = xrange(-3, 3)
    res = []
    for x0 in valueRange:
        for y0 in valueRange:
            for x1 in valueRange:
                for y1 in valueRange:
                    z0c = complex(x0,y0)
                    z1c = complex(x1,y1)
                    z0p = pycomplex(x0,y0)
                    z1p = pycomplex(x1,y1)
                    res.append((z0c, z1c, z0p, z1p))

    return res




class TestComplex(unittest.TestCase):

    def test_wrongInit1(self):
        "Compare wrong init. with CPython."
        
        try:
            complex("1", "1")
        except TypeError:
            pass
        else:
            raise TestFailed, 'complex("1", "1")'

        try:
            pycomplex("1", "1")
        except TypeError:
            pass
        else:
            raise TestFailed, 'complex("1", "1")'


    def test_wrongInit2(self):
        "Compare wrong init. with CPython."
        
        try:
            complex(1, "1")
        except TypeError:
            pass
        else:
            raise TestFailed, 'complex(1, "1")'

        try:
            pycomplex(1, "1")
        except TypeError:
            pass
        else:
            raise TestFailed, 'complex(1, "1")'


    def test_wrongInitFromString(self):
        "Compare string init. with CPython."

        if complex("  3.14+J  ") != 3.14+1j:
            raise TestFailed, 'complex("  3.14+J  )"'
        if not equal(pycomplex("  3.14+J  "), pycomplex(3.14,1)):
            raise TestFailed, 'complex("  3.14+J  )"'


    def test_wrongInitFromUnicodeString(self):
        "Compare unicode string init. with CPython."

        if have_unicode:
            if complex(unicode("  3.14+J  ")) != 3.14+1j:
                raise TestFailed, 'complex(u"  3.14+J  )"'
            if not equal(pycomplex(unicode("  3.14+J  ")), pycomplex(3.14, 1)):
                raise TestFailed, 'complex(u"  3.14+J  )"'


    def test_class(self):
        "Compare class with CPython."
        
        class Z:
            def __complex__(self):
                return 3.14j
        z = Z()
        if complex(z) != 3.14j:
            raise TestFailed, 'complex(classinstance)'

        if not equal(complex(z), pycomplex(0, 3.14)): 
            raise TestFailed, 'complex(classinstance)'


    def test_add_sub_mul_div(self):
        "Compare add/sub/mul/div with CPython."
        
        for (z0c, z1c, z0p, z1p) in enumerate():
            mc = z0c*z1c
            mp = z0p*z1p
            assert equal(mc, mp)

            sc = z0c+z1c
            sp = z0p+z1p
            assert equal(sc, sp)

            dc = z0c-z1c
            dp = z0p-z1p
            assert equal(dc, dp)

            if not equal(z1c, complex(0,0)): 
                try:
                    qc = z0c/z1c
                    qp = z0p/z1p
                    assert equal(qc, qp)
                except AssertionError:
                    print "c: (%s/%s) = (%s)" % (z0c, z1c, qc)
                    print "py:(%s/%s) = (%s)" % (z0p, z1p, qp)

                
    def test_special(self):
        "Compare special methods with CPython."
        
        for (x, y) in [(0,0), (0,1), (1,3.)]:
            zc = complex(x, y)
            zp = pycomplex(x, y)

            assert equal(zc, zp), "%s != %s" % (zc, zp)
            assert equal(-zc, -zp), "%s != %s" % (-zc, -zp)
            assert equal(+zc, +zp), "%s != %s" % (+zc, +zp)
            assert equal(abs(zc), abs(zp)), "%s != %s" % (abs(zc), abs(zp))
            assert equal(zc.conjugate(), zp.conjugate()), "%s != %s" % (zc.conjugate(), zp.conjugate())
            assert str(zc) == str(zp), "str(%s) != str(%s)" % (str(zc), str(zp))
            assert hash(zc) == hash(zp), "%s == hash(%s) != hash(%s) == %s" % (hash(zc), zc, zp, hash(zp))


    def test_divmod(self):
        "Compare divmod with CPython."
        
        for (z0c, z1c, z0p, z1p) in enumerate():
            mc = z0c*z1c
            mp = z0p*z1p
            assert equal(mc, mp)

            # divmod(9,4) = 2,1
            if not equal(z1c, complex(0,0)): 
                try:
                    ddc, mmc = divmod(z0c, z1c)
                    assert ddc*z1c + mmc == z0c
                    ddp, mmp = divmod(z0p, z1p)
                    # assert ddp*z1p + mmp == z0p
                    assert equal(ddc, ddp)
                    assert equal(mmc, mmp)
                except AssertionError:
                    print "c: divmod(%s,%s) = (%s,%s)" % (z0c, z1c, ddc,mmc)
                    print "py:divmod(%s,%s) = (%s,%s)" % (z0p, z1p, ddp,mmp)


    def test_mod(self):
        "Compare mod with CPython."
        
        for (z0c, z1c, z0p, z1p) in enumerate():
            mc = z0c*z1c
            mp = z0p*z1p
            assert equal(mc, mp)

            if not equal(z1c, complex(0,0)): 
                try:
                    rc = z0c%z1c
                    rp = z0p%z1p
                    assert equal(rc, rp)
                except AssertionError:
                    print "c: %s%%%s = %s" % (z0c, z1c, rc)
                    print "py:%s%%%s = %s" % (z0p, z1p, rp)
                    

    def test_pow(self):
        "Compare pow with CPython."
        
        for (z0c, z1c, z0p, z1p) in enumerate():
            if not equal(z0c, 0j) and (z1c.imag != 0.0):
                pc = z0c**z1c
                pp = z0p**z1p
                assert equal(pc, pp)
                pc = z0c**z0c.real
                pp = z0p**z0p.real
                assert equal(pc, pp)
                                



def dm(self, other):
    # a divmod like used in complex.
    
    div = self/other
    print div
    div = complex(math.floor(div.real), 0.0)
    print div
    mod = self - div*other
    print mod
    return div, mod


def testNumericalInstability():
    x, y = -3+1j, -1-3j
    print x, y, divmod(x, y)
    print x/y
    print math.floor((x/y).real)+0j
    print

    x, y = complex(-3,1), complex(-1,-3)
    print x, y
    dm(x, y)




if __name__ == "__main__":
    unittest.main()
