"""
Basic dylink tests.   Nothing fancy.

"""


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols('dytestmodule1.r2py')


# Should be mapped in by above...
assert(x == 1)

dytestmodule2 = dy_import_module('dytestmodule2.r2py')

assert(dytestmodule2.x == 2)


# JAC: There seems to be a bug in how dylink support in a python file for 
# dispatch.  This is likely a repyportability issue because as I understand it,
# add_dy_support is supposed to allow the below call to work...
#callargs = ['dytestmoduleexitall.r2py']
#dy_dispatch_module()

# once the above is fixed, I should not reach here
# log("Should not reach here!  exitall call in dispatched code!")
