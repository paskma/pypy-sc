import sys


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
