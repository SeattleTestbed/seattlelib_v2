#this unit test checks the functionality of the arc cosh fuinction 

from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("math.r2py")


import math


# Checks values form 0 to +- 2 pi in intervals of pi/4
count = 0
while(count != 9):
  print "\n"
  print math.acosh((math_pi*count) / 4)
  print math_acosh((math_pi*count) / 4)
  print "\n"
  # print math.acosh((-math_pi*count) / 4)
  # print math_acosh((-math_pi*count) / 4)

  if(math_acosh((math_pi*count) / 4) != math.acosh((math_pi*count) / 4)):
    print ("[FAIL]: graphing the positive domain of cos was a failure")
  # if(math_acosh((-math_pi*count) / 4) != math.acosh((-math_pi*count) / 4)):
  #   print ("[FAIL]: graphing the negative domain of cos was a failure")
  count += 1
