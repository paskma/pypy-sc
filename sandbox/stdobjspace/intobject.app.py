def int_getattr(i, attr):
    if attr == "__class__":
        return int
    raise AttributeError, ....
