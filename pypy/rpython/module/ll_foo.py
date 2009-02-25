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

    @registering(foo.acquire_boot_lock)
    def register_foo_acquire_boot_lock(self):
        return extdef([], None, llimpl=None,
                      export_name='ll_foo.ll_foo_acquire_boot_lock')

    @registering(foo.release_boot_lock)
    def register_foo_release_boot_lock(self):
        return extdef([], None, llimpl=None,
                      export_name='ll_foo.ll_foo_release_boot_lock')

    @registering(foo.dumpln)
    def register_foo_dumpln(self):
        return extdef([str], None, llimpl=None,
                      export_name='ll_foo.ll_foo_dumpln')

    @registering(foo.jpf_random)
    def register_foo_jpf_random(self):
        return extdef([int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_jpf_random')

    @registering(foo.jpf_begin_atomic)
    def register_foo_jpf_begin_atomic(self):
        return extdef([], None, llimpl=None,
                      export_name='ll_foo.ll_foo_jpf_begin_atomic')

    @registering(foo.jpf_end_atomic)
    def register_foo_jpf_end_atomic(self):
        return extdef([], None, llimpl=None,
                      export_name='ll_foo.ll_foo_jpf_end_atomic')
