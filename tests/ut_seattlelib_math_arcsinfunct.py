#this unit test checks the functionality of the arc sin fuinction 


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("math.r2py")


import math


# Checks values from 0 to +- 1 in intervals of 0.1
count = 0.0
while(str(count) != str(1.0)):
  if(str(math_asin(count)) != str(math.asin(count))):
    print ("[FAIL]: graphing the positive domain of sin was a failure")
  if(str(math_asin(-count)) != str(math.asin(-count))):
    print ("[FAIL]: graphing the negative domain of sin was a failure")
  count += 0.1
