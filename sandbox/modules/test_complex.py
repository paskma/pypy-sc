# Python test set -- part 4a, built-in functions a-m

from test_support import *
import math, sys, types

from complexobject import complex as pycomplex


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
    

# check special methods like __add__, etc.

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


# redoing checks as previously written for C version

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


if complex("  3.14+J  ") != 3.14+1j:
    raise TestFailed, 'complex("  3.14+J  )"'

if not equal(pycomplex("  3.14+J  "), pycomplex(3.14,1)):
    raise TestFailed, 'complex("  3.14+J  )"'

if have_unicode:
    if complex(unicode("  3.14+J  ")) != 3.14+1j:
        raise TestFailed, 'complex(u"  3.14+J  )"'
    if not equal(pycomplex(unicode("  3.14+J  ")), pycomplex(3.14, 1)):
        raise TestFailed, 'complex(u"  3.14+J  )"'


class Z:
    def __complex__(self):
        return 3.14j
z = Z()
if complex(z) != 3.14j:
    raise TestFailed, 'complex(classinstance)'

if not equal(complex(z), pycomplex(0, 3.14)): 
   raise TestFailed, 'complex(classinstance)'


# check functions in Python version of cmath

import cmath
import cmathmodule

for x0 in xrange(-3, 3):
    for y0 in xrange(-3, 3):
        for x1 in xrange(-3, 3):
            for y1 in xrange(-3, 3):
                z0c = complex(x0,y0)
                z1c = complex(x1,y1)
                z0p = pycomplex(x0,y0)
                z1p = pycomplex(x1,y1)

                mc = z0c*z1c
                mp = z0p*z1p
                sc = z0c+z1c
                sp = z0p+z1p
                dc = z0c-z1c
                dp = z0p-z1p
                assert equal(mc, mp)
                assert equal(sc, sp)
                assert equal(dc, dp)

                if not equal(z0c, 0j) and (z1c.imag != 0.0):
                     pc = z0c**z1c
                     pp = z0p**z1p
                     assert equal(pc, pp)
                     pc = z0c**x0
                     pp = z0p**x0
                     assert equal(pc, pp)
                                
                for op in "sqrt acos acosh asin asinh atan atanh cos cosh exp".split():
                    if op == "atan" and equal(z0c, complex(0,-1)) or equal(z0c, complex(0,1)):
                        continue
                    if op == "atanh" and equal(z0c, complex(-1,0)) or equal(z0c, complex(1,0)):
                        continue
                    op0 = cmath.__dict__[op](z0c)
                    op1 = cmathmodule.__dict__[op](z0p)
                    assert equal(op0, op1)
                # need to also do this for log and log10...!

                # check divisions
                if equal(z0c, complex(0,0)) or equal(z1c, complex(0,0)):
                    continue
                assert equal(mc/z0c, mp/z0p)
                assert equal(mc/z1c, mp/z1p)
                
