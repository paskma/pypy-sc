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

    @registering(foo.allocate_lock)
    def register_foo_allocate_lock(self):
        return extdef([], int, llimpl=None,
                      export_name='ll_foo.ll_foo_allocate_lock')

    @registering(foo.acquire_lock)
    def register_foo_acquire_lock(self):
        return extdef([int], None, llimpl=None,
                      export_name='ll_foo.ll_foo_acquire_lock')

    @registering(foo.release_lock)
    def register_foo_release_lock(self):
        return extdef([int], None, llimpl=None,
                      export_name='ll_foo.ll_foo_release_lock')

    @registering(foo.dumpln)
    def register_foo_dumpln(self):
        return extdef([str], None, llimpl=None,
                      export_name='ll_foo.ll_foo_dumpln')
