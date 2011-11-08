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

# C interface for inspiration                     
#int simplenet_connect(const char * hostname, int port);
#int simplenet_read(int slotnumber);
#int simplenet_close(int slotnumber);
#int simplenet_write_buf(int slotnumber, const char * buf, int size);
#int simplenet_write_char(int slotnumber, int character);
#int simplenet_flush(int slotnumber);
#int simplenet_set_timeout(int slotnumber, int timeoutmillis);

    @registering(foo.simplenet_connect)
    def register_foo_simplenet_connect(self):
        return extdef([str, int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_connect')

    @registering(foo.simplenet_read)
    def register_foo_simplenet_read(self):
        return extdef([int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_read')

    @registering(foo.simplenet_close)
    def register_foo_simplenet_close(self):
        return extdef([int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_close')

    @registering(foo.simplenet_write_buf)
    def register_foo_simplenet_write_buf(self):
        return extdef([int, str], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_write_buf')

    @registering(foo.simplenet_write_char)
    def register_foo_simplenet_write_char(self):
        return extdef([int, int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_write_char')

    @registering(foo.simplenet_flush)
    def register_foo_simplenet_flush(self):
        return extdef([int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_flush')

    @registering(foo.simplenet_set_timeout)
    def register_foo_simplenet_set_timeout(self):
        return extdef([int, int], int, llimpl=None,
                      export_name='ll_foo.ll_foo_simplenet_set_timeout')
