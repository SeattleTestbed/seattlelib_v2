#this unit test checks the functionality of the file traced object 

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("strace.r2py")

import subprocess


fielobj = wrapped_openfile("hi.txt", True)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("openfile ('hi.txt', True)" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile ('hi.txt', True)")
if("emulfile.emulated_file object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")


# #write something using trace call
fielobj.writeat("asdfasdf",0)
process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()

#Check apicall to traced call
if("file.writeat" not in tracedcall):
	log("Trace api call failed to trace correct function, writeat")
if("(\'asdfasdf\', 0)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, fielobj.writeat(\'asdfasdf\',0)")
if("emulfile.emulated_file object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")



#close file using trace call
fielobj.close()

#open traced file
process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]


#Check apicall to traced call
if("file.close" not in tracedcall):
	log("Trace api call failed to trace correct function, close")
if("emulfile.emulated_file object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")


#open existing file with trace call
fielobj = wrapped_openfile("../hi.txt", True)

#open traced file
process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]


#Check apicall to traced call
if("openfile" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("(\'../hi.txt\', True)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, openfile(\'../hi.txt\', True)")
if("emulfile.emulated_file object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")

#read from file usiung trace call
fielobj.readat(0,4)

#open traced file
process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]



#Check apicall to traced call
if("file.readat" not in tracedcall):
	log("Trace api call failed to trace correct function, readat")
if("(0, 4)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, fileobj.readat (0, 4)")
if("emulfile.emulated_file object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")

#close file using trace call
fielobj.close()

#open traced file
process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]


#Check apicall to traced call
if("file.close" not in tracedcall):
	log("Trace api call failed to trace correct function, close")
if("emulfile.emulated_file object"not in tracedcall):
	log("Failed to trace trace correct function as correct object")

