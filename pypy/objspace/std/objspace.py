

class MultiMethod(object):

    def __init__(self, arity, operatorsymbol):
        self.arity = arity
        self.operatorsymbol = operatorsymbol
        self.dispatch_table = {}

    def register(self, function, *types):
        if types in self.dispatch_table:
            raise ValueError, "we already got one for %r" % (types,)
        self.dispatch_table[types] = function

    def __get__(self, space, cls):
        if space is None:
            return self  # <-------------------------- Hack
        return BoundMultiMethod(space, self)

    def buildchoices(self, types):
        """Build a list of all possible combinations of delegated types,
        sorted by cost."""
        result = []
        self.internal_buildchoices(types, (), (), result)
        result.sort()
        return result

    def internal_buildchoices(self, initialtypes,
                              currenttypes, currentdelegators, result):
        if len(currenttypes) == self.arity:
            try:
                function = self.dispatch_table[currenttypes]
            except KeyError:
                pass
            else:
                result.append((currentdelegators, function))
        else:
            nexttype = initialtypes[len(currenttypes)]
            self.internal_buildchoices(initialtypes, currenttypes + (nexttype,),
                                       currentdelegators + (None,), result)
            delegators = getattr(nexttype, "delegate_once", {})
            for othertype, delegator in delegators.items():
                self.internal_buildchoices(initialtypes,
                                           currenttypes + (othertype,),
                                           currentdelegators + (delegator,),
                                           result)


class BoundMultiMethod:

    def __init__(self, space, multimethod):
        self.space = space
        self.multimethod = multimethod

    def __call__(self, *args):
        if len(args) != self.multimethod.arity:
            raise TypeError, ("multimethod got %d arguments instead of %d" %
                              (len(args), self.multimethod.arity))
        initialtypes = tuple([a.__class__ for a in args])
        choicelist = self.multimethod.buildchoices(initialtypes)
        firstfailure = None
        for delegators, function in choicelist:
            newargs = []
            for delegator, arg in zip(delegators, args):
                if delegator is not None:
                    arg = delegator(self.space, arg)
                newargs.append(arg)
            try:
                return function(self.space, *newargs)
            except FailedToImplement, e:
                print "we got FailedToImplement", e
                if firstfailure is None:
                    firstfailure = e
        if firstfailure is None:
            print "TypeError! XXX raise something like <<<unsupported operand types for +: 'int' and 'str'>>>"
        else:
            print "really failed to implement", firstfailure
        STOPME


class FailedToImplement(Exception):
    "Signals the dispatcher to try on harder."


class StdObjectSpace:

    type    = MultiMethod(1, 'type')
    getiter = MultiMethod(1, 'iter')
    repr    = MultiMethod(1, 'repr')
    getattr = MultiMethod(2, 'getattr')
    setattr = MultiMethod(3, 'setattr')
    pow  = MultiMethod(3, '**')
    
    add = MultiMethod(2, '+')
    sub = MultiMethod(2, '-')

    def __init__(self):

        # add concrete apis:
        
        import concretespace
        self.int = concretespace.IntObjSpace(self)
        self.float = concretespace.FloatObjSpace(self)

        # add type objects to space:

        import intobject
        self.W_IntObject = intobject.W_IntObject
        import floatobject
        self.W_FloatObject = floatobject.W_FloatObject

        # install exceptions

        self.w_TypeError = None

    """

    culled from trivialspace: a frighteningly long list of things that
    will be implemented here, eventually

    wrap
    unwrap
    type
    checktype
    newtuple
    newlist
    newdict
    newslice
    getiter
    repr
    pow
    setattr
    delattr
    is_true
    getattr
    pos
    neg
    not_
    pos
    neg
    not_
    invert
    mul
    truediv
    floordiv
    div
    mod
    lshift
    rshift
    and_
    xor
    or_
    getitem
    setitem
    delitem
    inplace_pow
    inplace_mul
    inplace_truediv
    inplace_floordiv
    inplace_div
    inplace_mod
    inplace_add
    inplace_sub
    inplace_lshift
    inplace_rshift
    inplace_and
    inplace_or
    inplace_xor
    iternext
    newfunction
    apply
    in_
    not_in
    is_
    is_not
    exc_match
    richcompare

    """

