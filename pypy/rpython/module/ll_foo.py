import foo

from pypy.rpython.extfunc import BaseLazyRegistering, registering, extdef

class RegisterFoo(BaseLazyRegistering):
    def __init__(self):
        pass

    @registering(foo.bar)
    def register_foo_bar(self):

        return extdef([float], None, llimpl=None,
                      export_name='ll_foo.ll_foo_bar')

    @registering(foo.start_new_thread)
    def register_foo_start_new_thread(self):

        return extdef([], None, llimpl=None,
                      export_name='ll_foo.ll_foo_start_new_thread')