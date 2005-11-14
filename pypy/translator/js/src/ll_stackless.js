// Stackless helper data and code

slp_frame_stack_top    = null
slp_frame_stack_bottom = null
slp_resume_block       = 0

function ll_stack_too_big() {
    return false; // XXX TODO use call depth here!
}

/*
#define STANDALONE_ENTRY_POINT   slp_standalone_entry_point


typedef struct slp_frame_s {
  struct slp_frame_s *f_back;
  int state;
} slp_frame_t;

typedef struct {
  slp_frame_t header;
  void* p0;
} slp_frame_1ptr_t;

struct slp_state_decoding_entry_s {
  void *function;
  int signature;
};

#include "slp_defs.h"

// implementations

// int slp_restart_substate;
// long slp_retval_long;
// double slp_retval_double;
// void *slp_retval_voidptr;
*/

function slp_new_frame(state) {
  f        = new Object();
  f.f_back = null;
  f.state  = state;
  return f;
}

function ll_stackless_stack_unwind() {
    if (slp_frame_stack_top) {
        slp_frame_stack_top = null; //odd
    } else {
        slp_frame_stack_top = slp_frame_stack_bottom = slp_new_frame(0);
    }
}
ll_stack_unwind = ll_stackless_stack_unwind

function    slp_return_current_frame_to_caller() {
  var   result = slp_frame_stack_top;
  slp_frame_stack_bottom.f_back = slp_new_frame(3);
  slp_frame_stack_top = slp_frame_stack_bottom = null;  // stop unwinding
  return result;
}

function slp_end_of_yielding_function() {
  slp_frame_stack_top = slp_retval_voidptr;
  return null;
}

function ll_stackless_switch(c) {
	var f;
	var result;
	if (slp_frame_stack_top) {  //resume
	    // ready to do the switch.  The current (old) frame_stack_top is
	    // f.f_back, which we store where it will be found immediately
	    // after the switch
	    f = slp_frame_stack_top;
	    result = f.f_back;

	    // grab the saved value of 'c' and do the switch
	    slp_frame_stack_top = f.p0;
	    return result;
        }

	// first, unwind the current stack
	f = slp_new_frame(2);
	f.p0 = c;
	slp_frame_stack_top = slp_frame_stack_bottom = f;
	return null;
}
ll_stackless_switch__frame_stack_topPtr = ll_stackless_switch

// example function for testing

function ll_stackless_stack_frames_depth() {
    if (slp_frame_stack_top) {
        f = slp_frame_stack_top;
        slp_frame_stack_top = null;
        for (var result = 0;f;result++) {
           f = f.f_back;
        }
        return result;
    } else {
	slp_frame_stack_top = slp_frame_stack_bottom = slp_new_frame(1);
	return -1;
    }
}

/*
#include "slp_state_decoding.h"

void slp_main_loop(void)
{
  int state, signature;
  slp_frame_t* pending;
  slp_frame_t* back;
  void* fn;

  while (1)
    {
      slp_frame_stack_bottom = null;
      pending = slp_frame_stack_top;

      while (1)
        {
          back = pending.f_back;
          state = pending.state;
          fn = slp_state_decoding_table[state].function;
          signature = slp_state_decoding_table[state].signature;
          if (fn != null)
            slp_restart_substate = 0;
          else
            {
              slp_restart_substate = signature;
              state -= signature;
              fn = slp_state_decoding_table[state].function;
              signature = slp_state_decoding_table[state].signature;
            }

          switch (signature) {

#include "slp_signatures.h"

	  }

          free(pending);  // consumed by the previous call
          if (slp_frame_stack_top)
            break;
          if (!back)
            return;
          pending = back;
          slp_frame_stack_top = pending;
        }
      // slp_frame_stack_bottom is usually non-null here, apart from
      // when returning from switch()
      if (slp_frame_stack_bottom)
        {
          assert(slp_frame_stack_bottom.f_back == null);
          slp_frame_stack_bottom.f_back = back;
        }
    }
}

int slp_standalone_entry_point(RPyListOfString *argv)
{
	int result;
	result = PYPY_STANDALONE(argv);
	if (slp_frame_stack_bottom) {
		slp_main_loop();
		result = (int) slp_retval_long;
	}
	return result;
}
*/

// End of Stackless helper data and code

