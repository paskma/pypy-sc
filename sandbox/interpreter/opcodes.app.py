import sys, new

#def prepare_raise0():
#    ...
#def prepare_raise1(type):
#    ...
#def prepare_raise2(type,value):
#    ...
#def prepare_raise3(type,value, traceback):
#    ...
    
def build_class(methods, bases, name):
    return classobj(name, bases, methods)

def print_expr(x):
    try:
        displayhook = sys.displayhook
    except AttributeError:
        raise RuntimeError, "lost sys.displayhook"
    displayhook(x)


def file_softspace(file, newflag):
    softspace = getattr(file, "softspace", False)
    try:
        stream.softspace = newflag
    except AttributeError:
        pass
    return softspace

def print_item_to(x, stream):
    if file_softspace(stream, False):
        stream.write(" ")
    # XXX add unicode handling
    stream.write(str(x))
    # XXX add softspaces

def print_item(x):
    try:
        stream = sys.stdout
    except AttributeError:
        raise RuntimeError, "lost sys.stdout"
    print_item_to(x, stream)

def print_newline_to(stream):
    stream.write("\n")
    file_softspace(stream, False)

def print_newline():
    try:
        stream = sys.stdout
    except AttributeError:
        raise RuntimeError, "lost sys.stdout"
    print_newline_to(stream)

def import_name(builtins, modulename, globals, locals, fromlist):
    try:
        import_ = builtins["__import__"]
    except KeyError:
        raise ImportError, "__import__ not found"
    import_(modulename, globals, locals, fromlist)

def import_all_from(module, locals):
    try:
        all = module.__all__
    except AttributeError:
        try:
            dict = module.__dict__
        except AttributeError:
            raise ImportError, ("from-import-* object has no __dict__ "
                                "and no __all__")
        all = dict.keys()
        skip_leading_underscores = True
    else:
        skip_leading_underscores = False
    for name in all:
        if skip_leading_underscores and name[0]=='_':
            continue
        locals[name] = getattr(module, name)

def import_from(module, name):
    try:
        return getattr(module, name)
    except AttributeError:
        raise ImportError, "cannot import name '%s'" % name

def load_name(name, locals, globals, builtins):
    try:
        return locals[name]
    except KeyError:
        try:
            return globals[name]
        except KeyError:
            try:
                return builtins[name]
            except KeyError:
                raise NameError, "name '%s' is not defined" % name

def load_closure(locals, name):
    # this assumes that 'locals' is an extended dictionary with a
    # 'cell' method to explicitely access a cell
    return locals.cell(name)

def concatenate_arguments(args, extra_args):
    return args + tuple(extra_args)

def concatenate_keywords(kw, extra_kw):
    if not isinstance(extra_kw, dict):
        raise TypeError, "argument after ** must be a dictionary"
    result = kw.copy()
    for key, value in extra_kw.items():
        if key in result:
            # XXX fix error message
            raise TypeError, ("got multiple values "
                              "for keyword argument '%s'" % key)
        result[key] = value
    return result
