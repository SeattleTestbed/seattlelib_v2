"""
Test the tcp_time library's tcp_time_updatetime().
"""
#pragma repy restrictions.default dylink.r2py
time_interface = dy_import_module("time_interface.r2py")
tcp_time = dy_import_module("tcp_time.r2py")

timeport = list(getresources()[0]["connport"])[0]

try:
  time_interface.time_updatetime(timeport)
  time_interface.time_gettime()
except time_interface.TimeError, err:
  log("[FAILED]: TCP time failed for following reason: " + str(err))
