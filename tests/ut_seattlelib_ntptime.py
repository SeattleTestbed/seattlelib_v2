"""
<Purpose>
  Test the ntp_time library which now uses
  Repy V2 network API calls.
  Function Tested:
    ntp_time_updatetime() in ntp_time.repy
"""
    
import repyhelper
repyhelper.translate_and_import("ntp_time.repy")

try:
  time_updatetime(12345)

  time_gettime()

except TimeError, err:
  log("[FAILED]: NTP time failed for following reason: " + str(err))