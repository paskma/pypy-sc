import dis, pypy, pyframe


class unaryoperation:
    def __init__(self, operationname):
        self.operationname = operationname
    def __call__(self, frame):
        operation = getattr(f.space, self.operationname)
        v = f.valuestack.pop()
        x = operation(v)
        f.valuestack.push(x)

class binaryoperation:
    def __init__(self, operationname):
        self.operationname = operationname
    def __call__(self, frame):
        operation = getattr(f.space, self.operationname)
        w = f.valuestack.pop()
        v = f.valuestack.pop()
        x = operation(v, w)
        f.valuestack.push(x)


################################################################
##  Implementation of the opcodes
##

def LOAD_FAST(f, varindex):
    varname = f.getname(varindex)
    x = f.locals[varname]
    f.valuestack.push(x)

def LOAD_CONST(f, constindex):
    x = f.getconstant(constindex)
    f.valuestack.push(x)

def STORE_FAST(f, varindex):
    v = f.valuestack.pop()
    varname = f.getname(varindex)
    f.locals[varname] = v

def POP_TOP(f):
    f.valuestack.pop()

def ROT_TWO(f):
    v = f.valuestack.pop()
    w = f.valuestack.pop()
    f.valuestack.push(v)
    f.valuestack.push(w)

def ROT_THREE(f):
    v = f.valuestack.pop()
    w = f.valuestack.pop()
    x = f.valuestack.pop()
    f.valuestack.push(v)
    f.valuestack.push(x)
    f.valuestack.push(w)

def ROT_FOUR(f):
    u = f.valuestack.pop()
    v = f.valuestack.pop()
    w = f.valuestack.pop()
    x = f.valuestack.pop()
    f.valuestack.push(u)
    f.valuestack.push(x)
    f.valuestack.push(w)
    f.valuestack.push(v)

def DUP_TOP(f):
    v = f.valuestack.top()
    f.valuestack.push(v)

def DUP_TOPX(f, itemcount):
    assert 1 <= itemcount <= 5, "limitation of the current interpreter"
    for i in range(itemcount):
        v = f.valuestack.top(-itemcount)
        f.valuestack.push(v)

UNARY_POSITIVE = unaryoperation("pos")
UNARY_NEGATIVE = unaryoperation("neg")
UNARY_NOT      = unaryoperation("not_")
UNARY_CONVERT  = unaryoperation("repr")
UNARY_INVERT   = unaryoperation("invert")

BINARY_POWER    = binaryoperation("pow")
BINARY_MULTIPLY = binaryoperation("mul")
BINARY_TRUE_DIVIDE  = binaryoperation("truediv")
BINARY_FLOOR_DIVIDE = binaryoperation("floordiv")
BINARY_DIVIDE       = binaryoperation("div")
BINARY_MODULO       = binaryoperation("mod")
BINARY_ADD      = binaryoperation("add")
BINARY_SUBTRACT = binaryoperation("sub")
BINARY_SUBSCR   = binaryoperation("getitem")
BINARY_LSHIFT   = binaryoperation("lshift")
BINARY_RSHIFT   = binaryoperation("rshift")
BINARY_AND = binary("and_")
BINARY_XOR = binary("xor")
BINARY_OR  = binary("or_")

INPLACE_POWER    = binaryoperation("inplace_pow")
INPLACE_MULTIPLY = binaryoperation("inplace_mul")
INPLACE_TRUE_DIVIDE  = binaryoperation("inplace_truediv")
INPLACE_FLOOR_DIVIDE = binaryoperation("inplace_floordiv")
INPLACE_DIVIDE       = binaryoperation("inplace_div")
INPLACE_MODULO       = binaryoperation("inplace_mod")
INPLACE_ADD      = binaryoperation("inplace_add")
INPLACE_SUBTRACT = binaryoperation("inplace_sub")
INPLACE_LSHIFT   = binaryoperation("inplace_lshift")
INPLACE_RSHIFT   = binaryoperation("inplace_rshift")
INPLACE_AND = binary("inplace_and_")
INPLACE_XOR = binary("inplace_xor")
INPLACE_OR  = binary("inplace_or_")

def slice(f, v, w):
    w_slice = f.space.build_slice(v, w, None)
    u = f.valuestack.pop()
    x = f.space.getitem(u, w_slice)
    f.push(x)

def SLICE_0(f):
    w = None
    v = None
    slice(f, v, w)

def SLICE_1(f):
    w = None
    v = f.valuestack.pop()
    slice(f, v, w)

def SLICE_2(f):
    w = f.valuestack.pop()
    v = None
    slice(f, v, w)

def SLICE_3(f):
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    slice(f, v, w)

def storeslice(f, v, w):
    w_slice = f.space.build_slice(v, w, None)
    u = f.valuestack.pop()
    t = f.valuestack.pop()
    f.space.setitem(u, w_slice, t)

def STORE_SLICE_0(f):
    w = None
    v = None
    storeslice(f, v, w)

def STORE_SLICE_1(f):
    w = None
    v = f.valuestack.pop()
    storeslice(f, v, w)

def STORE_SLICE_2(f):
    w = f.valuestack.pop()
    v = None
    storeslice(f, v, w)

def STORE_SLICE_3(f):
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    storeslice(f, v, w)

def deleteslice(f, v, w):
    w_slice = f.space.build_slice(v, w, None)
    u = f.valuestack.pop()
    f.space.delitem(u, w_slice)

def DELETE_SLICE_0(f):
    w = None
    v = None
    deleteslice(f, v, w)

def DELETE_SLICE_1(f):
    w = None
    v = f.valuestack.pop()
    deleteslice(f, v, w)

def DELETE_SLICE_2(f):
    w = f.valuestack.pop()
    v = None
    deleteslice(f, v, w)

def DELETE_SLICE_3(f):
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    deleteslice(f, v, w)

def STORE_SUBSCR(f):
    "v[w] = u"
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    u = f.valuestack.pop()
    f.space.setitem(v, w, u)

def DELETE_SUBSCR(f):
    "del v[w]"
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    f.space.delitem(v, w)

def PRINT_EXPR(f):
    v = f.valuestack.pop()
    pypy.applicationcall(f.space, "print_expr", [v])

def PRINT_ITEM_TO(f):
    w_stream = f.valuestack.pop()
    v = f.valuestack.pop()
    pypy.applicationcall(f.space, "print_item_to", [v, w_stream])

def PRINT_ITEM(f):
    v = f.valuestack.pop()
    pypy.applicationcall(f.space, "print_item", [v])

def PRINT_NEWLINE_TO(f):
    w_stream = f.valuestack.pop()
    pypy.applicationcall(f.space, "print_newline_to", [w_stream])

def PRINT_NEWLINE(f):
    pypy.applicationcall(f.space, "print_newline", [])

def BREAK_LOOP(f):
    raise pyframe.BreakLoop

def CONTINUE_LOOP(f, oparg):
    raise pyframe.ContinueLoop

def RAISE_VARARGS(f, oparg):
    if oparg == 0:
        pypy.applicationcall(f.space, "raise0")
    elif oparg == 1:
        w = f.valuestack.pop()
        pypy.applicationcall(f.space, "raise1", [w])
    elif oparg == 2:
        v = f.valuestack.pop()
        w = f.valuestack.pop()
        pypy.applicationcall(f.space, "raise2", [v, w])
    elif oparg == 3:
        u = f.valuestack.pop()
        v = f.valuestack.pop()
        w = f.valuestack.pop()
        pypy.applicationcall(f.space, "raise3", [u, v, w])
    else:
        raise pyframe.BytecodeCorruption

def LOAD_LOCALS(f):
    x = f.space.wrap(f.locals)
    f.valuestack.push(x)

def RETURN_VALUE(f):
    v_returnvalue = f.valuestack.pop()
    raise pyframe.ReturnValue(v_returnvalue)

def YIELD_VALUE(f):
    v_yieldedvalue = f.valuestack.pop()
    raise pyframe.YieldValue(v_yieldedvalue)
YIELD_STMT = YIELD_VALUE  # misnamed in dis.opname

def EXEC_STMT(f):
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    u = f.valuestack.pop()
    NotImplementedYet  # XXX

def POP_BLOCK(f):
    block = f.blockstack.pop()
    f.clearvaluestack(block.initialstackdepth)

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
