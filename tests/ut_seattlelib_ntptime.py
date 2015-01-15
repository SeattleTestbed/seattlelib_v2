"""
<Purpose>
  Test the ntp_time library which now uses
  Repy V2 network API calls.
  Function Tested:
    ntp_time_updatetime() in ntp_time.r2py
"""
#pragma repy restrictions.default dylink.r2py    
#from repyportability import *
#add_dy_support(locals())

time_interface = dy_import_module("time_interface.r2py")
ntp_time = dy_import_module("ntp_time.r2py")
timeport = list(getresources()[0]["connport"])[0]
try:
  
  time_interface.time_updatetime(timeport)

  time_interface.time_gettime()

except time_interface.TimeError, err:
  log("[FAILED]: NTP time failed for following reason: " + str(err))
