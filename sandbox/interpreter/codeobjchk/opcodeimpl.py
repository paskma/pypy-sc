from __future__ import nested_scopes
import dis


class placeholder:
    def __init__(self, s):
        self.s = s
    def __repr__(self):
        return "[%s]" % self.s
    __str__ = __repr__

class callsite:
    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args
    def __repr__(self):
        args = [str(a) for a in self.args]
        return "[%s(%s)]" % (self.fn, ', '.join(args))
    __str__ = __repr__

class callobj(callsite):
    pass

class callint(callsite):
    pass

NULL = placeholder("NULL")


def binary(cfn):
    def generic_binary(f):
        w = f.pop()
        v = f.pop()
        x = callobj(cfn, v, w)
        f.push(x)
    return generic_binary

def unary(cfn):
    def generic_unary(f):
        v = f.pop()
        x = callobj(cfn, v)
        f.push(x)
    return generic_unary

################################################################


def LOAD_FAST(f, oparg):
    x = f.getlocal(oparg)
    f.push(x)

def LOAD_CONST(f, oparg):
    x = f.getconst(oparg)
    f.push(x)

def STORE_FAST(f, oparg):
    v = f.pop()
    f.setlocal(oparg, v)

def POP_TOP(f):
    f.pop()

def ROT_TWO(f):
    v = f.pop()
    w = f.pop()
    f.push(v)
    f.push(w)

def ROT_THREE(f):
    v = f.pop()
    w = f.pop()
    x = f.pop()
    f.push(v)
    f.push(x)
    f.push(w)

def ROT_FOUR(f):
    u = f.pop()
    v = f.pop()
    w = f.pop()
    x = f.pop()
    f.push(u)
    f.push(x)
    f.push(w)
    f.push(v)

def DUP_TOP(f):
    v = f.top()
    f.push(v)

def DUP_TOPX(f, oparg):
    assert 1 <= oparg <= 5, "limitation of the current interpreter"
    for i in range(oparg):
        v = f.top(-oparg)
        f.push(v)

UNARY_POSITIVE = unary("PyNumber_Positive")
UNARY_NEGATIVE = unary("PyNumber_Negative")
UNARY_NOT      = unary("unary_not")
UNARY_CONVERT  = unary("PyObject_Repr")
UNARY_INVERT   = unary("PyNumber_Invert")

BINARY_POWER    = binary("binary_power")
BINARY_MULTIPLY = binary("PyNumber_Multiply")
BINARY_TRUE_DIVIDE  = binary("PyNumber_TrueDivide")
BINARY_FLOOR_DIVIDE = binary("PyNumber_FloorDivide")
BINARY_DIVIDE       = BINARY_TRUE_DIVIDE   # assume -Qnew behavior (2.3)
BINARY_MODULO = binary("PyNumber_Modulo")
BINARY_ADD = binary("PyNumber_Add")
BINARY_SUBTRACT = binary("PyNumber_Subtract")
BINARY_SUBSCR = binary("PyObject_GetItem")
BINARY_LSHIFT = binary("PyNumber_Lshift")
BINARY_RSHIFT = binary("PyNumber_Rshift")
BINARY_AND = binary("PyNumber_And")
BINARY_XOR = binary("PyNumber_Xor")
BINARY_OR = binary("PyNumber_Or")

INPLACE_POWER    = binary("inplace_power")
INPLACE_MULTIPLY = binary("PyNumber_InPlaceMultiply")
INPLACE_TRUE_DIVIDE  = binary("PyNumber_InPlaceTrueDivide")
INPLACE_FLOOR_DIVIDE = binary("PyNumber_InPlaceFloorDivide")
INPLACE_DIVIDE       = INPLACE_TRUE_DIVIDE   # assume -Qnew behavior (2.3)
INPLACE_MODULO = binary("PyNumber_InPlaceModulo")
INPLACE_ADD = binary("PyNumber_InPlaceAdd")
INPLACE_SUBTRACT = binary("PyNumber_InPlaceSubtract")
INPLACE_LSHIFT = binary("PyNumber_InPlaceLshift")
INPLACE_RSHIFT = binary("PyNumber_Rshift")
INPLACE_AND = binary("PyNumber_InPlaceAnd")
INPLACE_XOR = binary("PyNumber_InPlaceXor")
INPLACE_OR = binary("PyNumber_InPlaceOr")

def Slice(f, v, w):
    u = f.pop()
    x = callobj("apply_slice", u, v, w)
    f.push(x)

def SLICE_0(f):
    w = NULL
    v = NULL
    Slice(f, v, w)

def SLICE_1(f):
    w = NULL
    v = f.pop()
    Slice(f, v, w)

def SLICE_2(f):
    w = f.pop()
    v = NULL
    Slice(f, v, w)

def SLICE_3(f):
    w = f.pop()
    v = f.pop()
    Slice(f, v, w)

def StoreSlice(f, v, w):
    u = f.pop()
    t = f.pop()
    callint("assign_slice", u, v, w, t)

def STORE_SLICE_0(f):
    w = NULL
    v = NULL
    StoreSlice(f, v, w)

def STORE_SLICE_1(f):
    w = NULL
    v = f.pop()
    StoreSlice(f, v, w)

def STORE_SLICE_2(f):
    w = f.pop()
    v = NULL
    StoreSlice(f, v, w)

def STORE_SLICE_3(f):
    w = f.pop()
    v = f.pop()
    StoreSlice(f, v, w)

def DeleteSlice(f, v, w):
    u = f.pop()
    callint("delete_slice", u, v, w)

def DELETE_SLICE_0(f):
    w = NULL
    v = NULL
    DeleteSlice(f, v, w)

def DELETE_SLICE_1(f):
    w = NULL
    v = f.pop()
    DeleteSlice(f, v, w)

def DELETE_SLICE_2(f):
    w = f.pop()
    v = NULL
    DeleteSlice(f, v, w)

def DELETE_SLICE_3(f):
    w = f.pop()
    v = f.pop()
    DeleteSlice(f, v, w)

def STORE_SUBSCR(f):
    w = f.pop()
    v = f.pop()
    u = f.pop()
    callint("PyObject_SetItem", v, w, u)

def DELETE_SUBSCR(f):
    w = f.pop()
    v = f.pop()
    callint("PyObject_DelItem", v, w)

def PRINT_EXPR(f):
    v = f.pop()
    callint("print_expr", v)

def PrintItemTo(f, stream):
    v = f.pop()
    callint("print_item_to", v, stream)

def PRINT_ITEM_TO(f):
    PrintItemTo(f, f.pop())

def PRINT_ITEM(f):
    PrintItemTo(f, None)

def PrintNewlineTo(f, stream):
    callint("print_newline_to", stream)

def PRINT_NEWLINE_TO(f):
    PrintNewlineTo(f, f.pop())

def PRINT_NEWLINE(f):
    PrintNewlineTo(f, None)

def BREAK_LOOP(f):
    while 1:
        b = f.blockpop()
        f.clearstack(b)
        if b.b_type == "SETUP_LOOP":
            f.next_instr = b.b_handler
            break

def CONTINUE_LOOP(f, oparg):
    while 1:
        b = f.blockpop()
        if b.b_type == "SETUP_LOOP":
            f.blocksetup(b.b_type, b.b_handler, b.b_level)
            f.next_instr = oparg
            break

def RAISE_VARARGS(f, oparg):
    u = v = w = NULL
    assert oparg <= 3
    if oparg >= 3:
        u = f.pop()
    if oparg >= 2:
        v = f.pop()
    if oparg >= 1:
        w = f.pop()
    callint("do_raise", w, v, u)
    raise f.ExitLoop

def LOAD_LOCALS(f):
    x = f.getflocals()
    f.push(x)

def RETURN_VALUE(f):
    retval = f.pop()
    raise f.WhyReturn, retval

def YIELD_VALUE(f):
    retval = f.pop()
    callsite("YIELD_VALUE_NOW", retval)
YIELD_STMT = YIELD_VALUE  # misnamed in dis.opname

def EXEC_STMT(f):
    w = f.pop()
    v = f.pop()
    u = f.pop()
    callint("exec_statement", u, v, w)

def POP_BLOCK(f):
    b = f.blockpop()
    f.clearstack(b)

def END_FINALLY(f):
    if f.top() is None:
        f.pop()
    else:
        finallylevel = f.finallylevel.pop()
        assert f.stack_level() == finallylevel
        raise f.ExitLoop

def BUILD_CLASS(f):
    u = f.pop()
    v = f.pop()
    w = f.pop()
    x = callobj("build_class", u, v, w)
    f.push(x)

def STORE_NAME(f, oparg):
    w = f.getname(oparg)
    v = f.pop()
    callint("PyDict_SetItem", f.getflocals(), w, v)

def DELETE_NAME(f, oparg):
    w = f.getname(oparg)
    callint("PyDict_DelItem", f.getflocals(), w)

def UNPACK_SEQUENCE(f, oparg):
    v = f.pop()
    for i in xrange(oparg):
        w = placeholder("sequence item %d" % i)
        f.push(w)
    callsite("...XXX UNPACKING...")

def STORE_ATTR(f, oparg):
    w = f.getname(oparg)
    v = f.pop()
    u = f.pop()
    callint("PyObject_SetAttr", v, w, u)

def DELETE_ATTR(f, oparg):
    w = f.getname(oparg)
    v = f.pop()
    callint("delete_attr", v, w)

def STORE_GLOBAL(f, oparg):
    w = f.getname(oparg)
    v = f.pop()
    callint("PyDict_SetItem", f.getfglobals(), w, v)

def DELETE_GLOBAL(f, oparg):
    w = f.getname(oparg)
    callint("PyDict_DelItem", f.getfglobals(), w)

def LOAD_NAME(f, oparg):
    w = f.getname(oparg)
    x = callobj("PyDict_GetItem", f.getflocals(), w)
    f.push(x)

def LOAD_GLOBAL(f, oparg):
    w = f.getname(oparg)
    x = callobj("load_global", f.getfglobals(), f.getfbuiltins(), w)
    f.push(x)

def DELETE_FAST(f, oparg):
    x = f.getlocal(oparg)
    f.setlocal(oparg, NULL)

def LOAD_CLOSURE(f, oparg):
    x = f.getfreevar(oparg)
    f.push(x)

def LOAD_DEREF(f, oparg):
    x = f.getderef(oparg)
    f.push(x)

def STORE_DEREF(f, oparg):
    w = f.pop()
    f.setderef(oparg, w)

def BUILD_TUPLE(f, oparg):
    x = callobj("PyTuple_New", oparg)
    for i in xrange(oparg):
        v = f.pop()
        callsite("PyTuple_SetItem", x, oparg-1-i, v)
    f.push(x)

def BUILD_LIST(f, oparg):
    x = callobj("PyList_New", oparg)
    for i in xrange(oparg):
        v = f.pop()
        callsite("PyList_SetItem", x, oparg-1-i, v)
    f.push(x)

def BUILD_MAP(f, oparg):
    assert oparg == 0     # for future extension
    x = callobj("PyDict_New")
    f.push(x)

def LOAD_ATTR(f, oparg):
    w = f.getname(oparg)
    v = f.pop()
    x = callobj("PyObject_GetAttr", v, w)
    f.push(x)

def COMPARE_OP(f, oparg):
    w = f.pop()
    v = f.pop()
    op = dis.cmp_op[oparg]
    assert op != "BAD"   # why is this in cmp_op?
    x = callobj("cmp_outcome", oparg, v, w)
    f.push(x)

def IMPORT_NAME(f, oparg):
    w = f.getname(oparg)
    u = f.pop()
    if u is not None:
        assert type(u) in (tuple, list)   # exact type check
        for name in u:
            assert type(name) is str  # exact type check
    x = callobj("import_name", f.getfbuiltins(),
                w, f.getfglobals(), f.getflocals(), u)
    f.push(x)

def IMPORT_STAR(f):
    v = f.pop()
    callint("import_star", v)

def IMPORT_FROM(f, oparg):
    w = f.getname(oparg)
    v = f.top()
    x = callobj("import_from", v, w)
    f.push(x)

def JUMP_FORWARD(f, oparg):
    f.next_instr += oparg

def JUMP_IF_FALSE(f, oparg):
    v = f.top()
    #if false:
    f2 = f.copy()
    f2.next_instr += oparg
    #if true:
    pass

def JUMP_IF_TRUE(f, oparg):
    v = f.top()
    #if true:
    f2 = f.copy()
    f2.next_instr += oparg
    #if false:
    pass

def JUMP_ABSOLUTE(f, oparg):
    f.next_instr = oparg

def GET_ITER(f):
    v = f.pop()
    x = callobj("PyObject_GetIter", v)
    f.push(x)

def FOR_ITER(f, oparg):
    v = f.top()
    x = callobj("PyIter_Next", v)
    # if x is not NULL
    f2 = f.copy()
    f2.push(x)
    # else iterator ended normally
    v = f.pop()
    f.next_instr += oparg

def FOR_LOOP(f, oparg):
    raise ValueError, "FOR_LOOP is deprecated and unsafe"

def SETUP_LOOP(f, oparg):
    # break:
    f2 = f.copy()
    f2.next_instr = f2.next_instr + oparg
    # normal path
    f.blocksetup("SETUP_LOOP", f.next_instr + oparg, f.stack_level())

def SETUP_EXCEPT(f, oparg):
    # except:
    f2 = f.copy()
    f2.next_instr = f2.next_instr + oparg
    f2.push(placeholder("exc_traceback"))
    f2.push(placeholder("exc_value"))
    f2.push(placeholder("exc_type"))
    f2.finallylevel.append(f2.stack_level())
    # normal path
    f.blocksetup("SETUP_EXCEPT", f.next_instr + oparg, f.stack_level())

def SETUP_FINALLY(f, oparg):
    # finally:  (only the case with three stack objects pushed, exc val tb)
    f2 = f.copy()
    f2.next_instr = f2.next_instr + oparg
    f2.push(placeholder("exc_traceback"))
    f2.push(placeholder("exc_value"))
    f2.push(placeholder("exc_type"))
    f2.finallylevel.append(f2.stack_level())
    # normal path
    f.blocksetup("SETUP_FINALLY", f.next_instr + oparg, f.stack_level())

def CALL_FUNCTION(f, oparg):
    na = oparg & 0xff
    nk = (oparg>>8) & 0xff
    n = na + 2 * nk
    for i in range(n):
        f.pop()  # arguments
    func = f.pop()
    x = placeholder("call %s" % func)
    f.push(x)

def CALL_FUNCTION_VAR(f, oparg):
    f.pop()  # vararg
    CALL_FUNCTION(f, oparg)

def CALL_FUNCTION_KW(f, oparg):
    f.pop()  # kw
    CALL_FUNCTION(f, oparg)

def CALL_FUNCTION_VAR_KW(f, oparg):
    f.pop()  # kw
    f.pop()  # vararg
    CALL_FUNCTION(f, oparg)

def MAKE_FUNCTION(f, oparg):
    f.pop()  # code object
    for i in xrange(oparg):
        f.pop()  # defaults
    x = placeholder("new function")
    f.push(x)

def MAKE_CLOSURE(f, oparg):
    codeobj = f.pop()  # code object
    nfree = len(codeobj.co_freevars)
    for i in xrange(nfree):
        f.pop()  # closure
    for i in xrange(oparg):
        f.pop()  # defaults
    x = placeholder("new closure")
    f.push(x)

def BUILD_SLICE(f, oparg):
    assert oparg == 2 or oparg == 3   # future extension
    if oparg == 3:
        w = f.pop()
    else:
        w = NULL
    v = f.pop()
    u = f.pop()
    x = placeholder("PySlice_New(%s, %s, %s)" % (u, v, w))
    f.push(x)

def SET_LINENO(f, oparg):
    pass

def EXTENDED_ARG(f, oparg):
    opcode = f.nextop()
    oparg = oparg<<16 | f.nextarg()
    dispatch_arg(f, oparg)


################################################################

dispatch_table = {}
for i in range(256):
    opname = dis.opname[i].replace('+', '_')
    if opname in globals():
        dispatch_table[i] = globals()[opname]
    elif not opname.startswith('<') and i>0:
        print "* Warning, missing opcode %s" % opname

def dispatch_noarg(f, opcode):
    try:
        fn = dispatch_table[opcode]
    except KeyError:
        raise KeyError, "missing opcode %s" % dis.opname[opcode]
    fn(f)

def dispatch_arg(f, opcode, oparg):
    assert oparg >= 0
    try:
        fn = dispatch_table[opcode]
    except KeyError:
        raise KeyError, "missing opcode %s" % dis.opname[opcode]
    fn(f, oparg)
