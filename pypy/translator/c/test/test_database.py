import autopath, sys
from pypy.rpython.lltype import *
from pypy.rpython.rtyper import RPythonTyper
from pypy.translator.translator import Translator
from pypy.translator.c.database import LowLevelDatabase
from pypy.objspace.flow.model import Constant, Variable, SpaceOperation
from pypy.objspace.flow.model import Block, Link, FunctionGraph


def dump_on_stdout(database):
    print '/*********************************/'
    for node in database.structdeflist:
        for line in node.definition():
            print line
    print
    for node in database.globalcontainers():
        for line in node.forward_declaration():
            print line
    for node in database.globalcontainers():
        print
        for line in node.implementation():
            print line


def test_primitive():
    db = LowLevelDatabase()
    assert db.get(5) == '5'
    assert db.get(True) == '1'

def test_struct():
    db = LowLevelDatabase()
    S = GcStruct('test', ('x', Signed))
    s = malloc(S)
    s.x = 42
    assert db.get(s).startswith('&g_')
    assert db.containernodes.keys() == [s._obj]
    assert db.structdefnodes.keys() == [S]

def test_inlined_struct():
    db = LowLevelDatabase()
    S = GcStruct('test', ('x', Struct('subtest', ('y', Signed))))
    s = malloc(S)
    s.x.y = 42
    assert db.get(s).startswith('&g_')
    assert db.containernodes.keys() == [s._obj]
    assert len(db.structdefnodes) == 2
    assert S in db.structdefnodes
    assert S.x in db.structdefnodes

def test_complete():
    db = LowLevelDatabase()
    T = GcStruct('subtest', ('y', Signed))
    S = GcStruct('test', ('x', GcPtr(T)))
    s = malloc(S)
    s.x = malloc(T)
    s.x.y = 42
    assert db.get(s).startswith('&g_')
    assert db.containernodes.keys() == [s._obj]
    db.complete()
    assert len(db.containernodes) == 2
    assert s._obj in db.containernodes
    assert s.x._obj in db.containernodes
    assert len(db.structdefnodes) == 2
    assert S in db.structdefnodes
    assert S.x.TO in db.structdefnodes

def test_codegen():
    db = LowLevelDatabase()
    U = Struct('inlined', ('z', Signed))
    T = GcStruct('subtest', ('y', Signed))
    S = GcStruct('test', ('x', GcPtr(T)), ('u', U), ('p', NonGcPtr(U)))
    s = malloc(S)
    s.x = malloc(T)
    s.x.y = 42
    s.u.z = -100
    s.p = cast_flags(NonGcPtr(U), s.u)
    db.get(s)
    db.complete()
    dump_on_stdout(db)

def test_codegen_2():
    db = LowLevelDatabase()
    A = GcArray(('x', Signed))
    S = GcStruct('test', ('aptr', GcPtr(A)))
    a = malloc(A, 3)
    a[0].x = 100
    a[1].x = 101
    a[2].x = 102
    s = malloc(S)
    s.aptr = a
    db.get(s)
    db.complete()
    dump_on_stdout(db)

def test_codegen_3():
    db = LowLevelDatabase()
    A = GcStruct('varsizedstuff', ('x', Signed), ('y', Array(('i', Signed))))
    S = GcStruct('test', ('aptr', GcPtr(A)),
                         ('anitem', NonGcPtr(A.y.OF)),
                         ('anarray', NonGcPtr(A.y)))
    a = malloc(A, 3)
    a.x = 99
    a.y[0].i = 100
    a.y[1].i = 101
    a.y[2].i = 102
    s = malloc(S)
    s.aptr = a
    s.anitem = cast_flags(NonGcPtr(A.y.OF), a.y[1])
    s.anarray = cast_flags(NonGcPtr(A.y), a.y)
    db.get(s)
    db.complete()
    dump_on_stdout(db)

def test_func_simple():
    # -------------------- flowgraph building --------------------
    #     def f(x):
    #         return x+1
    x = Variable("x")
    x.concretetype = Signed
    result = Variable("result")
    result.concretetype = Signed
    one = Constant(1)
    one.concretetype = Signed
    op = SpaceOperation("int_add", [x, one], result)
    block = Block([x])
    graph = FunctionGraph("f", block)
    block.operations.append(op)
    block.closeblock(Link([result], graph.returnblock))
    graph.getreturnvar().concretetype = Signed
    # --------------------         end        --------------------
    
    F = FuncType([Signed], Signed)
    f = functionptr(F, "f", graph=graph)
    db = LowLevelDatabase()
    db.get(f)
    db.complete()
    dump_on_stdout(db)

    S = GcStruct('testing', ('fptr', NonGcPtr(F)))
    s = malloc(S)
    s.fptr = f
    db = LowLevelDatabase()
    db.get(s)
    db.complete()
    dump_on_stdout(db)

def test_untyped_func():
    def f(x):
        return x+1
    t = Translator(f)
    graph = t.getflowgraph()

    F = FuncType([GcPtr(PyObject)], GcPtr(PyObject))
    f = functionptr(F, "f", graph=graph)
    db = LowLevelDatabase()
    db.get(f)
    db.complete()
    dump_on_stdout(db)

    S = GcStruct('testing', ('fptr', NonGcPtr(F)))
    s = malloc(S)
    s.fptr = f
    db = LowLevelDatabase()
    db.get(s)
    db.complete()
    dump_on_stdout(db)

def test_function_call():
    def g(x, y):
        return x-y
    def f(x):
        return g(1, x)
    t = Translator(f)
    a = t.annotate([int])
    RPythonTyper(t.annotator).specialize()

    F = FuncType([Signed], Signed)
    f = functionptr(F, "f", graph=t.getflowgraph())
    db = LowLevelDatabase()
    db.get(f)
    db.complete()
    dump_on_stdout(db)

def test_func_as_pyobject():
    def f(x):
        return x+1
    t = Translator(f)
    a = t.annotate([int])
    rtyper = RPythonTyper(t.annotator)
    rtyper.specialize()

    db = LowLevelDatabase(rtyper)
    db.get(pyobjectptr(f))
    db.complete()
    dump_on_stdout(db)
