

class W_SliceObject(object):
    __slots__ = ['start', 'stop', 'step']
    def __init__(self, start, stop, step):
        self.w_start = w_start
        self.w_stop = w_stop
        self.w_step = w_step
    def indices(self, space, w_length):
        length = space.int_as_long(w_length)
        
        if self.w_step == space.w_None:
            step = 1
        elif isinstance(self.w_step, W_IntObject):
            step = self.w_step.intval
            if step == 0:
                raise OperationError(
                    space.w_ValueError,
                    space.W_StringObject("slice step cannot be zero"))
        else:
            raise OperationError(space.w_TypeError)
            
        if step < 0:
            defstart = length - 1
            defstop = -1
        else:
            defstart = 0
            defstop = length
            
        if self.w_start is space.w_None:
            start = defstart
        else:
            start = space.eval_slice_index(self.w_start)
            if start < 0:
                start = start + length
                if start < 0:
                    if step < 0:
                        start = -1
                    else:
                        start = 0
                elif start >= length:
                    if step < 0:
                        start = length - 1
                    else:
                        start = length

       if 
