"""
<Purpose>
  Test the tcp_time library which now uses
  Repy V2 network API calls.
  Function Tested:
    tcp_time_updatetime() in ntp_time.r2py
"""
from repyportability import *
add_dy_support(locals())

time_interface = dy_import_module("time_interface.r2py")
tcp_time = dy_import_module("tcp_time.r2py")

try:
  time_interface.time_updatetime(12345)

  time_interface.time_gettime()

except time_interface.TimeError, err:
  log("[FAILED]: TCP time failed for following reason: " + str(err))
