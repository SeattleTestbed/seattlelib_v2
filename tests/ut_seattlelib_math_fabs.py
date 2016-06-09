#this unit test checks the functionality of the absolute value function 

from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("math.r2py")

import math

# Checks values form -10 to 10 in intervals of 1
count = 0
while(count != 10):
  if(math.fabs(count) != math_fabs(count)):
     print ("[FAIL]: Compairing absolute value was a failure")
  if(math.fabs(-count) != math_fabs(-count)):
     print ("[FAIL]: Compairing absolute value was a failure")
  count += 1