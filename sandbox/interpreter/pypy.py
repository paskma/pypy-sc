import sys, operator


# use the operator module as the trivial, wrapping-less,
# exception-handling-less object space.
operator.wrap = operator.unwrap = lambda x: x
operator.type = type
trivialspace = operator


class OperationError(Exception):
    """Interpreter-level exception that signals an exception that should be
    sent to the application level.
    
    Arguments are the object-space exception class and value."""




def applicationcall(space, functionname, argumentslist):
    w_function = applicationfunction(f.space, functionname)
    w_arguments = f.space.new_tuple(argumentslist)
    return f.space.apply(w_function, w_arguments)
