#this unit test checks the functionality of the strace socket object

from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("strace.r2py")

import subprocess

localip = "127.0.0.1"
localport1 = 12345
localport2 = 12347
targetip = "127.0.0.1"
targetport = 12346
timeout = 1.0

conn = wrapped_openconnection(targetip, targetport, localip, localport1, timeout)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("openconnection" not in tracedcall):
	log("Trace api call failed to trace correct function, openconnection")
if("('127.0.0.1', 12346, '127.0.0.1', 12345, 1.0)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, openconnection('127.0.0.1', 12346, '127.0.0.1', 12345, 1.0)")
if("emulcomm.EmulatedSocket" not in tracedcall):
	log("Failed to trace trace correct function as correct object")



conn.send("Hi from repy program!")


# 0.01771 socket.send <emulcomm.EmulatedSocket instance at 0x7f0bc3905758> ('Hi from repy program!',) = 21

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("socket.send" not in tracedcall):
	log("Trace api call failed to trace correct function, socket.send")
if("('Hi from repy program!',)" not in tracedcall and "21" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, send('Hi from repy program!',)")
if("emulcomm.EmulatedSocket" not in tracedcall):
	log("Failed to trace trace correct function as correct object")


conn.recv(21)

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("socket.recv" not in tracedcall):
	log("Trace api call failed to trace correct function, socket.send")
if("(21,)" not in tracedcall):
	log("Trace api call failed to trace correct function with correct parameters, send('Hi from repy program!',)")
if("emulcomm.EmulatedSocket" not in tracedcall):
	log("Failed to trace trace correct function as correct object")



conn.close()

process = subprocess.Popen('', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output = process.stdout.readlines()
tracedcall = output[0]

#Check apicall to traced call
if("socket.close" not in tracedcall):
	log("Trace api call failed to trace correct function, socket.send")
if("emulcomm.EmulatedSocket" not in tracedcall):
	log("Failed to trace trace correct function as correct object")