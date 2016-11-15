#this unit test checks the functionality of the arc tan fuinction 


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("math.r2py")

import math

# Checks values from 0 to +- 1 in intervals of 0.1
count = 0.0
while(str(count) != str(1.0)):
  if(math_atan(count) != math.atan(count)):
    if(str(math_atan(count)) != str(math.atan(count))):
      print ("[FAIL]: graphing the positive domain of tan was a failure")
  if(math_atan(-count) != math.atan(-count)):
    if(str(math_atan(-count)) != str(math.atan(-count))):
      print ("[FAIL]: graphing the negative domain of tan was a failure")
  count += 0.1


# Checks values form 0 to +- 10 in intervals of 1
count = 0
while(count != 1):
  if(math_atan(count) != math.atan(count)):
    if(str(math_atan(count)) != str(math.atan(count))):
      print ("[FAIL]: graphing the positive domain of tan was a failure")
  if(math_atan(-count) != math.atan(-count)):
    if(str(math_atan(-count)) != str(math.atan(-count))):
      print ("[FAIL]: graphing the negative domain of tan was a failure")
  count += 1