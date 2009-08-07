
def bar(x):
	print "Should not be here."
	pass

def start_new_thread():
	print "Should not be here."
	pass

def allocate_lock():
	print "Should not be here."
	return 0

def acquire_lock(lockNum):
	print "Should not be here."
	pass

def release_lock(lockNum):
	print "Should not be here."
	pass

def acquire_boot_lock():
	print "Should not be here."
	pass

def release_boot_lock():
	print "Should not be here."
	pass

def dumpln(s):
	print "Should not be here."
	pass

def jpf_random(i):
	print "Should not be here."
	return 1

def jpf_begin_atomic():
	print "Should not be here."
	pass

def jpf_end_atomic():
	print "Should not be here."
	pass
