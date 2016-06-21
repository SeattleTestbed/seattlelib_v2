#this unit test checks the functionality of the lock traced object

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("strace.r2py")

import subprocess


#create a lock
PRINT_LOCK = wrapped_createlock()

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("createlock" not in tracedcall):
	log("Trace api call failed to trace correct function, createlock")
if("emulmisc.emulated_lock object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")

PRINT_LOCK.acquire(True)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("lock.acquire" not in tracedcall):
	log("Trace api call failed to trace correct function, lock.acquire")
if("(True,)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct paramaters, lock.acquire(True)")
if("emulmisc.emulated_lock object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")



PRINT_LOCK.release()

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("lock.release" not in tracedcall):
	log("Trace api call failed to trace correct function, createlock")
if("emulmisc.emulated_lock object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")