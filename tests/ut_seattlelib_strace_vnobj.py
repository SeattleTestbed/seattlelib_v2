#this unit test checks the functionality of the strace virtual namespace object 

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("strace.r2py")

import subprocess

#most of code taken from ut_repyv2api_virtualnamespace-eval.py

# Small code snippet, safe
safe_code = "meaning_of_life = 42\n"

# Try to make the safe virtual namespace
safe_virt = wrapped_virtual_namespace(safe_code, "Test VN")


process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("VirtualNamespace(...)" not in tracedcall):
	log("Trace api call failed to trace correct function, VirtualNamespace(...)")
if("virtual_namespace.VirtualNamespace " not in tracedcall):
	log("Failed to trace trace correct function as correct object")



# Create a execution context
context = SafeDict()

# Evaluate
context_2 = safe_virt.evaluate(context)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("VirtualNamespace.evaluate" not in tracedcall):
	log("Trace api call failed to trace correct function, evaluate")
if("virtual_namespace.VirtualNamespace " not in tracedcall):
	log("Failed to trace trace correct function as correct object")


# Check that the context is the same
if context is not context_2:
  log("Error! Context mis-match!",'\n')

# Check for the meaning of life
if "meaning_of_life" not in context:
  log("Meaning of life is undefined! Existential error!",'\n')