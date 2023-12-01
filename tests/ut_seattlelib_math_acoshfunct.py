#this unit test checks the functionality of the acosh function


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("math.r2py")


import math


# Checks values form 1 to 9
count = 1
while(count != 9):
  if(math_acosh(count) != math.acosh(count)):
    if(str(math_acosh(count)) != str(math.acosh(count))):
      print ("[FAIL]: graphing the positive domain of cos was a failure")
  count += 1
