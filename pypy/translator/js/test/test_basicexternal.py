
""" BasicExternal testers
"""

import py

from pypy.rpython.ootypesystem.bltregistry import MethodDesc, BasicExternal, described
from pypy.translator.js.test.runtest import compile_function, check_source_contains

class A(BasicExternal):
    @described(retval=3)
    def some_code(self, var="aa"):
        pass

a = A()

class B(object):
    pass

def test_decorator():
    def dec_fun():
        a.some_code("aa")
    
    fun = compile_function(dec_fun, [])
    check_source_contains(fun, "\.some_code")

def test_basicexternal_element():
    def be_fun():
        b = B()
        b.a = a
        b.a.some_code("aa")
    
    fun = compile_function(be_fun, [])
    check_source_contains(fun, "\.some_code")

def test_basicexternal_raise():
    py.test.skip("Constant BasicExternals not implemented")
    def raising_fun():
        try:
            b = B()
        except:
            pass
        else:
            return 3

    fun = compile_function(raising_fun, [])
    assert fun() == 3

class C(BasicExternal):
    @described(retval=3)
    def f(self):
        pass

c = C()

def test_basicexternal_raise_method_call():
    def raising_method_call():
        try:
            c.f()
        except:
            pass

    fun = compile_function(raising_method_call, [])
    assert len(C._methods) == 1
    assert 'f' in C._methods

class D(BasicExternal):
    _fields = {
        'a': {"aa":"aa"},
        'b': ["aa"],
    }

D._fields['c'] = [D(),D()]

d = D()

def test_basicexternal_list():
    def getaa(item):
        return d.c[item]
    
    def return_list(i):
        one = getaa(i)
        if one:
            two = getaa(i + 3)
            return two
        return one

    fun2 = compile_function(return_list, [int])

def test_basicextenal_dict():
    def return_dict():
        return d.a

    fun1 = compile_function(return_dict, [])

def test_method_call():
    py.test.skip("Fails")
    class Meth(BasicExternal):
        @described(retval=3)
        def meth(self):
            return 8
            
    l = []
    
    def callback(i):
        l.append(i)
    
    meth = Meth()
    meth.meth(callback)
    assert l[0] == 8
