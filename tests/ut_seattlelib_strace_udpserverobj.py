#this unit test checks the functionality of the udp server traced object 

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("strace.r2py")

import subprocess



udpserverobj = wrapped_listenformessage(getmyip(), 12345)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("listenformessage" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("('192.168.183.128', 12345)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, openfile('../hi.txt', True)")
if("emulcomm.UDPServerSocket"not in tracedcall):
	log("Failed to trace trace correct function as correct object")

try:
	udpserverobj.getmessage()
except SocketWouldBlockError:
#expected
	pass

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("UDPServerSocket.getmessage" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("emulcomm.UDPServerSocket"not in tracedcall):
	log("Failed to trace trace correct function as correct object")


udpserverobj.close()

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("UDPServerSocket.close" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("emulcomm.UDPServerSocket"not in tracedcall):
	log("Failed to trace trace correct function as correct object")
