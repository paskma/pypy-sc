"""
Global Interpreter Lock.
"""

# This module adds a global lock to an object space.
# If multiple threads try to execute simultaneously in this space,
# all but one will be blocked.  The other threads get a chance to run
# from time to time, using the hook yield_thread().

from pypy.module.thread import ll_thread as thread
from pypy.module.thread.error import wrap_thread_error
from pypy.interpreter.miscutils import Action
from pypy.module.thread.threadlocals import OSThreadLocals
from pypy.rlib.objectmodel import invoke_around_extcall
from pypy.rlib.rposix import get_errno, set_errno

class GILThreadLocals(OSThreadLocals):
    """A version of OSThreadLocals that enforces a GIL."""
    ll_GIL = thread.null_ll_lock

    def setup_threads(self, space):
        """Enable threads in the object space, if they haven't already been."""
        if not self.ll_GIL:
            try:
                self.ll_GIL = thread.allocate_ll_lock()
            except thread.error:
                raise wrap_thread_error(space, "can't allocate GIL")
            thread.acquire_NOAUTO(self.ll_GIL, True)
            self.enter_thread(space)   # setup the main thread
            # add the GIL-releasing callback as an action on the space
            space.pending_actions.append(GILReleaseAction(self))
            result = True
        else:
            result = False      # already set up

        # add the GIL-releasing callback around external function calls.
        #
        # XXX we assume a single space, but this is not quite true during
        # testing; for example, if you run the whole of test_lock you get
        # a deadlock caused by the first test's space being reused by
        # test_lock_again after the global state was cleared by
        # test_compile_lock.  As a workaround, we repatch these global
        # fields systematically.
        spacestate.ll_GIL = self.ll_GIL
        invoke_around_extcall(before_external_call, after_external_call)
        return result

    def yield_thread(self):
        """Notification that the current thread is between two bytecodes:
        release the GIL for a little while."""
        # Other threads can run between the release() and the acquire()
        # implicit in the following external function call (which has
        # otherwise no effect).
        thread.yield_thread()


class GILReleaseAction(Action):
    """An action called when the current thread is between two bytecodes
    (so that it's a good time to yield some time to other threads).
    """
    repeat = True

    def __init__(self, threadlocals):
        self.threadlocals = threadlocals

    def perform(self):
        self.threadlocals.yield_thread()


class SpaceState:
    def _freeze_(self):
        self.ll_GIL = thread.null_ll_lock
        return False
spacestate = SpaceState()

# Fragile code below.  We have to preserve the C-level errno manually...

def before_external_call():
    # this function must not raise, in such a way that the exception
    # transformer knows that it cannot raise!
    e = get_errno()
    thread.release_NOAUTO(spacestate.ll_GIL)
    set_errno(e)
before_external_call._gctransformer_hint_cannot_collect_ = True

def after_external_call():
    e = get_errno()
    thread.acquire_NOAUTO(spacestate.ll_GIL, True)
    thread.gc_thread_run()
    set_errno(e)
after_external_call._gctransformer_hint_cannot_collect_ = True
