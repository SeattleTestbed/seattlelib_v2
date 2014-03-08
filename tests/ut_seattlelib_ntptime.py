"""
<Purpose>
  Test the ntp_time library which now uses
  Repy V2 network API calls.
  Function Tested:
    ntp_time_updatetime() in ntp_time.repy
"""
    
from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("ntp_time.repy")

try:
  time_updatetime(12345)

  time_gettime()

except TimeError, err:
  log("[FAILED]: NTP time failed for following reason: " + str(err))
