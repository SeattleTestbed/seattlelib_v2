"""
<Purpose>
  Test the sockettimeout library which now uses
  Repy V2 network API calls.
  Function Tested:
    tcpserversocket.getconnection() in sockettimeout.repy
"""


import repyhelper

repyhelper.translate_and_import("sockettimeout.repy")

# Create a listening socket that would timeout in 2 seconds.
servsocket = timeout_listenforconnection("127.0.0.1", 12345, 2)

# Accept new connections, should raise SocketTimeoutError if no connection
# is made within 2 seconds.
try:
  remoteip, remoteport, clisocket = servsocket.getconnection()
  clisocket.close()
except SocketTimeoutError, err:
  pass
else:
  log("[FAIL]: Socket did not timeout when listening for new connection.\n")
  

# gracefully close the server socket.
servsocket.close()