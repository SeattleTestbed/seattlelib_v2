#this unit test checks the functionality of the atanh function 


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("math.r2py")

import math

#Checks value from -1 to 1
count = 0.0
while(str(count) != str(1.0)):
  if(math_atanh(count) != math.atanh(count)):
    if(str(math_atanh(count)) != str(math.atanh(count))):
      print ("[FAIL]: graphing the positive domain of tan was a failure")
  if(math_atanh(-count) != str(math.atanh(-count))):
    if(str(math_atanh(count)) != str(math.atanh(count))):
      print ("[FAIL]: graphing the negative domain of tan was a failure")
  count += 0.1

