import dis
from opcodeimpl import dispatch_noarg, dispatch_arg, placeholder

CO_MAXBLOCKS = 20

CO_OPTIMIZED	= 0x0001
CO_NEWLOCALS	= 0x0002
CO_VARARGS	= 0x0004
CO_VARKEYWORDS	= 0x0008
CO_NESTED       = 0x0010
CO_GENERATOR    = 0x0020



class FrameBlock:
    "For try and loop blocks."

    def __init__(self, b_type, b_handler, b_level):
        self.b_type = b_type
        self.b_handler = b_handler
        self.b_level = b_level

    def key(self):
        return (self.b_type, self.b_handler, self.b_level)

    def __hash__(self):
        return hash(self.key())

    def __cmp__(self, other):
        assert isinstance(other, FrameBlock)
        return cmp(self.key(), other.key())

    def __repr__(self):
        return "%s@%d" % (self.b_type, self.b_level)


class Frame:
    "A frame object."
    
    class ExitLoop(Exception):
        pass
    class WhyReturn(ExitLoop):
        pass
    class ProtectedPop(Exception):
        pass
    
    def __init__(self, co, f=None):
        self.f_code = co
        self.f_nlocals = co.co_nlocals
        self.f_stacksize = co.co_stacksize
	self.f_ncellfrees = len(co.co_cellvars) + len(co.co_freevars)
        self.nfastlocals = self.f_nlocals + self.f_ncellfrees
        if f is None:
            self.f_blockstack = ()
            self.stack = []
            self.seen = {}
            self.next_instr = 0
            self.finallylevel = []
            self.siblings = []
        else:
            self.f_blockstack = f.f_blockstack
            self.stack = f.stack[:]
            self.seen = f.seen   # shared
            self.next_instr = f.next_instr
            self.finallylevel = f.finallylevel[:]
            self.siblings = f.siblings  # shared
        self.siblings.append(self)

    def nextop(self):
        c = self.f_code.co_code[self.next_instr]
        self.next_instr += 1
        return ord(c)

    def nextarg(self):
        lo = self.nextop()
        hi = self.nextop()
        return (hi<<8) + lo

    def getname(self, oparg):
        return self.f_code.co_names[oparg]

    def push(self, v):
        assert len(self.stack) < self.f_stacksize
        self.stack.append(v)

    def protectlevel(self):
        if self.f_blockstack:
            return self.f_blockstack[-1].b_level
        else:
            return 0

    def pop(self):
        assert len(self.stack) > self.protectlevel()
        if self.finallylevel and len(self.stack) == self.finallylevel[-1]:
            # POPping through the objects pushed by the exception handler
            # is allowed (case of except: not re-raising the exception)
            # but then no more END_FINALLY is allowed
            self.finallylevel.pop()
        return self.stack.pop()

    def top(self, n=1):
        return self.stack[-n]

    def blocksetup(self, *args):
        assert len(self.f_blockstack) < CO_MAXBLOCKS
        b = FrameBlock(*args)
        self.f_blockstack = self.f_blockstack + (b,)

    def blockpop(self):
        b = self.f_blockstack[-1]
        self.f_blockstack = self.f_blockstack[:-1]
        return b

    def clearstack(self, b):
        assert 0 <= b.b_level <= len(self.stack)
        assert b.b_level >= self.protectlevel()
        del self.stack[b.b_level:]

    def stack_level(self):
        return len(self.stack)

    def getlocal(self, i):
        assert 0 <= i < self.f_nlocals
        return placeholder("local %d" % i)

    def getfreevar(self, i):
        assert 0 <= i < self.f_ncellfrees
        return placeholder("freevar %d" % i)

    def getderef(self, i):
        assert 0 <= i < self.f_ncellfrees
        return placeholder("deref %d" % i)

    def getconst(self, i):
        return self.f_code.co_consts[i]

    def setlocal(self, i, value):
        assert 0 <= i < self.f_nlocals

    def setfreevar(self, i, value):
        assert 0 <= i < self.f_ncellfrees

    def setderef(self, i, value):
        assert 0 <= i < self.f_ncellfrees

    def getflocals(self):
        return placeholder("f->f_locals")

    def getfglobals(self):
        return placeholder("f->f_globals")

    def getfbuiltins(self):
        return placeholder("f->f_builtins")

    def eval_frame(self):
        try:
            while 1:
                key = self.next_instr, len(self.stack)
                if key in self.seen:
                    assert self.seen[key] == self.f_blockstack
                    break
                self.seen[key] = self.f_blockstack
                opcode = self.nextop()
                if opcode >= dis.HAVE_ARGUMENT:
                    oparg = self.nextarg()
                    dispatch_arg(self, opcode, oparg)
                else:
                    dispatch_noarg(self, opcode)
        except Frame.ExitLoop:
            pass

    def copy(self):
        return Frame(self.f_code, self)


def CheckCode(co):
    f1 = Frame(co)
    try:
        while f1.siblings:
            f = f1.siblings.pop()
            f.eval_frame()
    except:
        dis.dis(co)
        print "*** next_instr = %d" % f.next_instr
        print "*** block_stack = %s" % (f.f_blockstack,)
        print "*** stack = %s" % (f.stack,)
        raise


################################################################

if __name__ == '__main__':
    import sys, os
    
    modules = []
    for path in sys.path:
        if path.startswith(sys.prefix):
            try:
                dirlist = os.listdir(path)
            except OSError:
                continue
            for fn in dirlist:
                if fn.endswith(".py"):
                    modules.append(fn[:-3])
            break
    d = {}
    def reccheck(dict):
        for value in dict.values():
            if id(value) not in d:
                d[id(value)] = 1
                if isinstance(value, functiontype):
                    CheckCode(value.func_code)
                elif hasattr(value, '__dict__'):
                    reccheck(value.__dict__)

    functiontype = type(reccheck)

    for m in modules:
        if not m.startswith('__') and not d.has_key(m):
            d[m] = 1
            print m
            try:
                mo = __import__(m, globals(), locals(), ['__doc__'])
            except:
                print "(exception ignored)"
                continue
            reccheck(mo.__dict__)
