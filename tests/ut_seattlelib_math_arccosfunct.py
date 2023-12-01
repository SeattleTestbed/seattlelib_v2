#this unit test checks the functionality of the arc cos function 

from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("math.r2py")


import math


# Checks values from 0 to +- 2 pi in intervals of pi/4
count = 0.0
while(str(count) != str(1.0)):
  if(str(math_acos(count)) != str(math.acos(count))):
    print ("[FAIL]: graphing the positive domain of cos was a failure")
  if(str(math_acos(-count)) != str(math.acos(-count))):
    print ("[FAIL]: graphing the negative domain of cos was a failure")
  count += 0.1
