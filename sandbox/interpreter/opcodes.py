import dis, pypy, pyframe


# dynamically loaded application-space utilities
applicationfile = pypy.AppFile("opcodes.app.py")


class unaryoperation:
    def __init__(self, operationname):
        self.operationname = operationname
    def __call__(self, f):
        operation = getattr(f.space, self.operationname)
        v = f.valuestack.pop()
        x = operation(v)
        f.valuestack.push(x)

class binaryoperation:
    def __init__(self, operationname):
        self.operationname = operationname
    def __call__(self, f):
        operation = getattr(f.space, self.operationname)
        w = f.valuestack.pop()
        v = f.valuestack.pop()
        x = operation(v, w)
        f.valuestack.push(x)


################################################################
##  Implementation of the opcodes
##

def LOAD_FAST(f, varindex):
    varname = f.getlocalvarname(varindex)
    w_varname = f.space.wrap(varname)
    x = f.space.getitem(f.w_locals, w_varname)
    # XXX catch KeyError and make it a NameError
    f.valuestack.push(x)

def LOAD_CONST(f, constindex):
    x = f.getconstant(constindex)
    f.valuestack.push(x)

def STORE_FAST(f, varindex):
    varname = f.getlocalvarname(varindex)
    w_varname = f.space.wrap(varname)
    v = f.valuestack.pop()
    f.space.setitem(f.w_locals, w_varname, v)

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
BINARY_AND = binaryoperation("and_")
BINARY_XOR = binaryoperation("xor")
BINARY_OR  = binaryoperation("or_")

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
INPLACE_AND = binaryoperation("inplace_and_")
INPLACE_XOR = binaryoperation("inplace_xor")
INPLACE_OR  = binaryoperation("inplace_or_")

def slice(f, v, w):
    w_slice = f.space.new_slice(v, w, None)
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
    w_slice = f.space.new_slice(v, w, None)
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
    w_slice = f.space.new_slice(v, w, None)
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
    applicationfile.call(f.space, "print_expr", [v])

def PRINT_ITEM_TO(f):
    w_stream = f.valuestack.pop()
    v = f.valuestack.pop()
    applicationfile.call(f.space, "print_item_to", [v, w_stream])

def PRINT_ITEM(f):
    v = f.valuestack.pop()
    applicationfile.call(f.space, "print_item", [v])

def PRINT_NEWLINE_TO(f):
    w_stream = f.valuestack.pop()
    applicationfile.call(f.space, "print_newline_to", [w_stream])

def PRINT_NEWLINE(f):
    applicationfile.call(f.space, "print_newline", [])

def BREAK_LOOP(f):
    raise pyframe.BreakLoop

def CONTINUE_LOOP(f, startofloop):
    raise pyframe.ContinueLoop(startofloop)

def RAISE_VARARGS(f, nbargs):
    if nbargs == 0:
        applicationfile.call(f.space, "raise0")
    elif nbargs == 1:
        w = f.valuestack.pop()
        applicationfile.call(f.space, "raise1", [w])
    elif nbargs == 2:
        v = f.valuestack.pop()
        w = f.valuestack.pop()
        applicationfile.call(f.space, "raise2", [v, w])
    elif nbargs == 3:
        u = f.valuestack.pop()
        v = f.valuestack.pop()
        w = f.valuestack.pop()
        applicationfile.call(f.space, "raise3", [u, v, w])
    else:
        raise pyframe.BytecodeCorruption

def LOAD_LOCALS(f):
    f.valuestack.push(f.w_locals)

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
    block.cleanup(f)  # the block knows how to clean up the value stack

def END_FINALLY(f):
    # unlike CPython, the information on what to do at the end
    # of a 'finally' is not stored in the value stack, but in
    # the block stack, in a new dedicated block type which knows
    # how to restore the environment (exception, break/continue...)
    # at the beginning of the 'finally'.
    block = f.blockstack.pop()
    block.cleanup(f)

def BUILD_CLASS(f):
    u = f.valuestack.pop()
    v = f.valuestack.pop()
    w = f.valuestack.pop()
    x = applicationfile.call(f.space, "build_class", [u, v, w])
    f.push(x)

def STORE_NAME(f, varindex):
    varname = f.getname(varindex)
    w_varname = f.space.wrap(varname)
    v = f.valuestack.pop()
    f.space.setitem(f.w_locals, w_varname, v)

def DELETE_NAME(f, varindex):
    varname = f.getname(varindex)
    w_varname = f.space.wrap(varname)
    f.space.delitem(f.w_locals, w_varname)
    # XXX catch KeyError and make it a NameError

def UNPACK_SEQUENCE(f, itemcount):
    v = f.valuestack.pop()
    w_iterator = f.space.getiter(v)
    items = []
    for i in range(itemcount):
        try:
            w_item = f.space.iternext(w_iterator)
        except pypy.NoValue:
            if i == 1:
                plural = ""
            else:
                plural = "s"
            message = "need more than %d value%s to unpack" % (i, plural)
            w_exceptionclass = applicationfile.findobject(f.space, "ValueError")
            w_exceptionvalue = f.space.wrap(message)
            raise OperationError(w_exceptionclass, w_exceptionvalue)
        items.append(w_item)
    # check that we have exhausted the iterator now.
    try:
        f.space.iternext(w_iterator)
    except pypy.NoValue:
        pass
    else:
        w_exceptionclass = applicationfile.findobject(f.space, "ValueError")
        w_exceptionclass = f.space.wrap("too many values to unpack")
        raise OperationError(w_exceptionclass, w_exceptionvalue)
    items.reverse()
    for item in items:
        f.valuestack.push(item)

def STORE_ATTR(f, nameindex):
    "v.attributename = u"
    attributename = f.getname(nameindex)
    w_attributename = f.space.wrap(attributename)
    v = f.valuestack.pop()
    u = f.valuestack.pop()
    f.space.setattr(v, w_attributename, u)

def DELETE_ATTR(f, nameindex):
    "del v.attributename"
    attributename = f.getname(nameindex)
    w_attributename = f.space.wrap(attributename)
    v = f.valuestack.pop()
    f.space.delattr(v, w_attributename)

def STORE_GLOBAL(f, nameindex):
    varname = f.getname(nameindex)
    w_varname = f.space.wrap(varname)
    v = f.valuestack.pop()
    f.space.setitem(f.w_globals, w_varname, v)

def DELETE_GLOBAL(f, nameindex):
    varname = f.getname(nameindex)
    w_varname = f.space.wrap(varname)
    f.space.delitem(f.w_globals, w_varname)

def LOAD_NAME(f, nameindex):
    varname = f.getname(nameindex)
    w_varname = f.space.wrap(varname)
    x = applicationfile.call(f.space, "load_name",
                             [w_varname, f.w_locals, f.w_globals, f.w_builtins])
    f.valuestack.push(x)

def LOAD_GLOBAL(f, nameindex):
    varname = f.getname(nameindex)
    w_varname = f.space.wrap(varname)
    try:
        x = f.space.getitem(f.w_globals, w_varname)
    except OperationError, e:
        # catch KeyErrors
        w_exc_class, w_exc_value = e.args
        w_KeyError = applicationfile.findobject(f.space, "KeyError")
        w_match = f.space.richcompare(w_exc_class, w_KeyError, "exc match")
        if not f.space.is_true(w_match):
            raise
        # we got a KeyError, now look in the built-ins
        try:
            x = f.space.getitem(f.w_builtins, w_varname)
        except OperationError, e:
            # catch KeyErrors again
            w_exc_class, w_exc_value = e.args
            w_match = f.space.richcompare(w_exc_class, w_KeyError, "exc match")
            if not f.space.is_true(w_match):
                raise
            message = "global name '%s' is not defined" % varname
            w_exc_class = applicationfile.findobject(f.space, "NameError")
            w_exc_value = f.space.wrap(message)
            raise OperationError(w_exc_class, w_exc_value)
    f.valuestack.push(x)

def DELETE_FAST(f, varindex):
    varname = f.getlocalvarname(varindex)
    w_varname = f.space.wrap(varname)
    f.space.delitem(f.w_locals, w_varname)
    # XXX catch KeyError and make it a NameError

def LOAD_CLOSURE(f, varindex):
    # nested scopes: access the cell object
    # XXX at some point implement an explicit traversal of
    #     syntactically nested frames?
    varname = f.getfreevarname(varindex)
    w_varname = f.space.wrap(varname)
    x = applicationfile.call(f.space, "load_closure", [f.w_locals, w_varname])
    f.valuestack.push(x)

def LOAD_DEREF(f, varindex):
    # nested scopes: access a variable through its cell object
    varname = f.getfreevarname(varindex)
    w_varname = f.space.wrap(varname)
    x = f.space.getitem(f.w_locals, w_varname)
    # XXX catch KeyError and make it a NameError
    f.valuestack.push(x)

def STORE_DEREF(f, varindex):
    # nested scopes: access a variable through its cell object
    varname = f.getfreevarname(varindex)
    w_varname = f.space.wrap(varname)
    v = f.valuestack.pop()
    f.space.setitem(f.w_locals, w_varname, v)

def BUILD_TUPLE(f, itemcount):
    items = [f.valuestack.pop() for i in range(itemcount)]
    items.reverse()
    x = f.space.new_tuple(items)
    f.valuestack.push(x)

def BUILD_LIST(f, itemcount):
    items = [f.valuestack.pop() for i in range(itemcount)]
    items.reverse()
    x = f.space.new_list(items)
    f.valuestack.push(x)

def BUILD_MAP(f, zero):
    if zero != 0:
        raise pyframe.BytecodeCorruption
    x = f.space.new_dict([])
    f.valuestack.push(x)

def LOAD_ATTR(f, nameindex):
    "v.attributename"
    attributename = f.getname(nameindex)
    w_attributename = f.space.wrap(attributename)
    v = f.valuestack.pop()
    x = f.space.getattr(v, w_attributename)
    f.valuestack.push(x)

def COMPARE_OP(f, test):
    testnames = ["<", "<=", "==", "!=", ">", ">=",
                 "in", "not in", "is", "is not", "exc match"]
    testname = testnames[test]
    w = f.valuestack.pop()
    v = f.valuestack.pop()
    x = f.space.richcompare(v, w, testname)
    f.valuestack.push(x)

def IMPORT_NAME(f, nameindex):
    modulename = f.getname(nameindex)
    w_modulename = f.space.wrap(modulename)
    w_fromlist = f.valuestack.pop()
    x = applicationfile.call(f.space, "import_name",
                             [f.w_builtins, w_modulename, f.w_globals,
                              f.w_locals, w_fromlist])
    f.valuestack.push(x)

def IMPORT_STAR(f):
    w_module = f.valuestack.pop()
    applicationfile.call(f.space, "import_star",
                         [w_module, f.w_locals])

def IMPORT_FROM(f, nameindex):
    name = f.getname(nameindex)
    w_name = f.space.wrap(name)
    w_module = f.valuestack.top()
    x = applicationfile.call(f.space, "import_from", [w_module, w_name])
    f.valuestack.push(x)

def JUMP_FORWARD(f, stepby):
    f.next_instr += stepby

def JUMP_IF_FALSE(f, stepby):
    v = f.valuestack.top()
    if not f.space.is_true(v):
        f.next_instr += stepby

def JUMP_IF_TRUE(f, stepby):
    v = f.valuestack.top()
    if f.space.is_true(v):
        f.next_instr += stepby

def JUMP_ABSOLUTE(f, jumpto):
    f.next_instr = jumpto

def GET_ITER(f):
    v = f.valuestack.pop()
    x = f.space.getiter(v)
    f.valuestack.push(x)

def FOR_ITER(f, jumpby):
    w_iterator = f.valuestack.top()
    try:
        x = f.space.iternext(w_iterator)
    except pypy.NoValue:
        # iterator exhausted
        f.valuestack.pop()
        f.next_instr += jumpby
    else:
        f.valuestack.push(x)

#def FOR_LOOP(f, oparg):
#    removed

def SETUP_LOOP(f, offsettoend):
    block = pyframe.LoopBlock(f, f.next_instr + offsettoend)
    f.blockstack.push(block)

def SETUP_EXCEPT(f, offsettoend):
    block = pyframe.ExceptBlock(f, f.next_instr + offsettoend)
    f.blockstack.push(block)

def SETUP_FINALLY(f, offsettoend):
    block = pyframe.FinallyBlock(f, f.next_instr + offsettoend)
    f.blockstack.push(block)

def call_function_extra(f, oparg, with_varargs, with_varkw):
    n_arguments = oparg & 0xff
    n_keywords = (oparg>>8) & 0xff
    if with_varkw:
        w_varkw = f.valuestack.pop()
    if with_varargs:
        w_varargs = f.valuestack.pop()
    keywords = []
    for i in range(n_keywords):
        w_value = f.valuestack.pop()
        w_key   = f.valuestack.pop()
        keywords.append((w_value, w_key))
    arguments = [f.valuestack.pop() for i in range(n_arguments)]
    arguments.reverse()
    w_function  = f.valuestack.pop()
    w_arguments = f.space.new_tuple(arguments)
    w_keywords  = f.space.new_dict(keywords)
    if with_varargs:
        w_arguments = applicationfile.call(f.space, "concatenate_arguments",
                                           [w_arguments, w_varargs])
    if with_kwargs:
        w_keywords  = applicationfile.call(f.space, "concatenate_keywords",
                                           [w_keywords,  w_varkw])
    x = f.space.apply(w_function, w_arguments, w_keywords)
    f.valuestack.push(x)

def CALL_FUNCTION(f, oparg):
    call_function_extra(f, oparg, False, False)

def CALL_FUNCTION_VAR(f, oparg):
    call_function_extra(f, oparg, True,  False)

def CALL_FUNCTION_KW(f, oparg):
    call_function_extra(f, oparg, False, True)

def CALL_FUNCTION_VAR_KW(f, oparg):
    call_function_extra(f, oparg, True,  True)

def MAKE_FUNCTION(f, numdefaults):
    w_codeobj = f.valuestack.pop()
    defaultarguments = [f.valuestack.pop() for i in range(numdefaults)]
    defaultarguments.reverse()
    w_defaultarguments = f.space.new_tuple(defaultarguments)
    x = f.space.new_function(w_codeobj, w_defaultarguments)
    f.valuestack.push(x)

def MAKE_CLOSURE(f, numdefaults):
    w_codeobj = f.valuestack.pop()
    codeobj = f.space.unwrap(w_codeobj)
    nfreevars = len(codeobj.co_freevars)
    freevars = [f.valuestack.pop() for i in range(nfreevars)]
    freevars.reverse()
    w_freevars = f.space.new_tuple(freevars)
    defaultarguments = [f.valuestack.pop() for i in range(numdefaults)]
    defaultarguments.reverse()
    w_defaultarguments = f.space.new_tuple(defaultarguments)
    x = f.space.new_function(w_codeobj, w_defaultarguments, w_freevars)
    f.valuestack.push(x)

def BUILD_SLICE(f, numargs):
    if numargs == 3:
        w = f.valuestack.pop()
    elif numargs == 2:
        w = None
    else:
        raise pyframe.BytecodeCorruption
    v = f.valuestack.pop()
    u = f.valuestack.pop()
    x = f.space.new_slice(u, v, w)
    f.valuestack.push(x)

def SET_LINENO(f, lineno):
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
