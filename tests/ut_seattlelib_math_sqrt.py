#this unit test checks the functionality of the sqrt function

from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("math.r2py")

import math

# Checks values form 0 to 2 
count = 0.0
while(str(count) != str(2.0)):
  if(math.sqrt(count) != math_sqrt(count)):
    if(str(math.sqrt(count)) != str(math_sqrt(count))):
     print ("[FAIL]: Compairing sqrt was a failure")
  count += 0.1