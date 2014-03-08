"""
<Purpose>
  Test the centralizedadvertise_v2 library which now uses
  Repy V2 network API calls.
  Function Tested:
    v2centralizedadvertise_announce() and v2centralizedadvertise_lookup()
"""

from repyportability import *
add_dy_support(locals())

from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("centralizedadvertise_v2.repy")


# advertise some random key with arbitrary value...
v2centralizedadvertise_announce("test", "234389459", 10)

# avoids socket cleanup errors...
sleep(0.05)

# lookup the random key that we announced...
if not v2centralizedadvertise_lookup("test")[0] == "234389459":
  print "[FAIL]: centralizedadvertise returned different value than advertised."
