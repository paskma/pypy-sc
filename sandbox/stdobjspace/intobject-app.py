def int_getattr(i, attr):
    if attr == "__class__":
        return int
    raise AttributeError, "'int' object has no attribute '%s'" % attr