#this unit test checks the functionality of the tcp server traced object

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("strace.r2py")

import subprocess


tcpserverobj = wrapped_listenforconnection(getmyip(), 12345)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("listenforconnection" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("('192.168.183.128', 12345)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, openfile('../hi.txt', True)")
if("emulcomm.TCPServerSocket"not in tracedcall):
	log("Failed to trace trace correct function as correct object")

try:
	tcpserverobj.getconnection()
except SocketWouldBlockError:
#expected
	pass
	
process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("TCPServerSocket.getconnection" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("emulcomm.TCPServerSocket"not in tracedcall):
	log("Failed to trace trace correct function as correct object")


tcpserverobj.close()

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("TCPServerSocket.close" not in tracedcall):
	log("Trace api call failed to trace correct function, openfile")
if("emulcomm.TCPServerSocket"not in tracedcall):
	log("Failed to trace trace correct function as correct object")


# wrapped_openconnection("127.0.0.1", 12345, getmyip(),63100, 10)

