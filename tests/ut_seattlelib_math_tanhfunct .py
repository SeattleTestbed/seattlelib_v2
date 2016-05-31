#this unit test checks the functionality of the tanh function 


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("math.r2py")

import math


# Checks values from +-pi/4 to +- 2 pi in intervals of pi/4
count = 1
while(count != 9):
  if(math_tanh((math_pi*count) / 4) != math.tanh((math_pi*count) / 4)):
    if(str(math_tanh((math_pi*count) / 4)) != str(math.tanh((math_pi*count) / 4))):
      print ("[FAIL]: graphing the positive domain of tan was a failure")
  if(math_tanh((-math_pi*count) / 4) != math.tanh((-math_pi*count) / 4)):
    if(str(math_tanh((-math_pi*count) / 4)) != str(math.tanh((-math_pi*count) / 4))):
      print ("[FAIL]: graphing the negative domain of tan was a failure")
  count += 1

