"""This module is always available. It provides access to mathematical
functions for complex numbers."""

# Complex math module

# much code borrowed from mathmodule.c

import math
from complexobject import complex

M_PI = 3.141592653589793239

        

# constants
_one = complex(1., 0.)
_half = complex(0.5, 0.)
_i = complex(0., 1.)
_halfi = complex(0., 0.5)



def acos(x):
    """acos(x)

    Return the arc cosine of x."""
    
    # return c_neg(prodi(log(c_sum(x,c_prod(_i,sqrt(c_diff(_one,c_prod(x,x))))))))
    return -(prodi(log((x+(_i*sqrt((_one-(x*x))))))))


def acosh(x):
    """acosh(x)

    Return the hyperbolic arccosine of x."""

    z = complex()
    z = sqrt(_half)
    z = log(c_prod(z, c_sum(sqrt(c_sum(x,_one)),sqrt(c_diff(x,_one)))))
    return c_sum(z, z)


def asin(x):
    """asin(x)

    Return the arc sine of x."""
    
    # -i * log[(sqrt(1-x**2) + i*x]
    squared = c_prod(x, x)
    sqrt_1_minus_x_sq = sqrt(c_diff(_one, squared))
    return c_neg(prodi(log(c_sum(sqrt_1_minus_x_sq, prodi(x)))))


def asinh(x):
    """asinh(x)

    Return the hyperbolic arc sine of x."""
    
    z = complex()
    z = sqrt(_half)
    # z = log(c_prod(z, c_sum(sqrt(c_sum(x, _i)),sqrt(c_diff(x, _i)))))
    z = log((z * (sqrt(x+_i)+sqrt((x-_i)))  ))
    return c_sum(z, z)


def atan(x):
    """atan(x)
    
    Return the arc tangent of x."""
    
    # return c_prod(_halfi,log(c_quot(c_sum(_i,x),c_diff(_i,x))))
    return _halfi*log(((_i+x)/(_i-x)))


def atanh(x):
    """atanh(x)

    Return the hyperbolic arc tangent of x."""
    
    return c_prod(_half,log(c_quot(c_sum(_one,x),c_diff(_one,x))))


def cos(x):
    """cos(x)

    Return the cosine of x."""
    
    r = complex()
    r.real = math.cos(x.real)*math.cosh(x.imag)
    r.imag = -math.sin(x.real)*math.sinh(x.imag)
    return r


def cosh(x):
    """cosh(x)
    
    Return the hyperbolic cosine of x."""
    
    r = complex()
    r.real = math.cos(x.imag)*math.cosh(x.real)
    r.imag = math.sin(x.imag)*math.sinh(x.real)
    return r


def exp(x):
    """exp(x)
    
    Return the exponential value e**x."""
    
    r = complex()
    l = math.exp(x.real)
    r.real = l*math.cos(x.imag)
    r.imag = l*math.sin(x.imag)
    return r


def log(x):
    """log(x)

    Return the natural logarithm of x."""
    
    r = complex()
    l = math.hypot(x.real,x.imag)
    r.imag = math.atan2(x.imag, x.real)
    r.real = math.log(l)
    return r


def log10(x):
    """log10(x)

    Return the base-10 logarithm of x."""
    
    r = complex()
    l = math.hypot(x.real,x.imag)
    r.imag = math.atan2(x.imag, x.real)/log(10.)
    r.real = math.log10(l)
    return r


# internal function not available from Python
def prodi(x):
    r = complex()
    r.real = -x.imag
    r.imag = x.real
    return r


def sin(x):
    """sin(x)

    Return the sine of x."""
    
    r = complex()
    r.real = math.sin(x.real) * math.cosh(x.imag)
    r.imag = math.cos(x.real) * math.sinh(x.imag)
    return r


def sinh(x):
    """sinh(x)

    Return the hyperbolic sine of x."""
    
    r = complex()
    r.real = math.cos(x.imag) * math.sinh(x.real)
    r.imag = math.sin(x.imag) * math.cosh(x.real)
    return r


def sqrt(x):
    """sqrt(x)

    Return the square root of x."""
    
    r = complex()
    if x.real == 0. and x.imag == 0.:
        r = x
    else:
        s = math.sqrt(0.5*(math.fabs(x.real) + math.hypot(x.real,x.imag)))
        d = 0.5*x.imag/s
        if x.real > 0.:
            r.real = s
            r.imag = d
        elif x.imag >= 0.:
            r.real = d
            r.imag = s
        else:
            r.real = -d
            r.imag = -s
    return r


def tan(x):
    """tan(x)

    Return the tangent of x."""

    r = complex()
    sr = math.sin(x.real)
    cr = math.cos(x.real)
    shi = math.sinh(x.imag)
    chi = math.cosh(x.imag)
    rs = sr * chi
    is_ = cr * shi
    rc = cr * chi
    ic = -sr * shi
    d = rc*rc + ic * ic
    r.real = (rs*rc + is_*ic) / d
    r.imag = (is_*rc - rs*ic) / d
    return r


def tanh(x):
    """tanh(x)

    Return the hyperbolic tangent of x."""
    
    r = complex()
    si = math.sin(x.imag)
    ci = math.cos(x.imag)
    shr = math.sinh(x.real)
    chr = math.cosh(x.real)
    rs = ci * shr
    is_ = si * chr
    rc = ci * chr
    ic = si * shr
    d = rc*rc + ic*ic
    r.real = (rs*rc + is_*ic) / d
    r.imag = (is_*rc - rs*ic) / d
    return r

