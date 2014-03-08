"""
<Purpose>
  Test the udpcentralizedadvertise library which now uses
  Repy V2 network API calls.
  Function Tested:
    udpcentralizedadvertise_announce() and udpcentralizedadvertise_lookup()
"""


from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("udpcentralizedadvertise.repy")


# advertise some random key with arbitrary value...
udpcentralizedadvertise_announce("test", "234389459", 10)

# avoids socket cleanup error...
sleep(0.05)

# lookup the random key that we announced...
if not udpcentralizedadvertise_lookup("test")[0] == "234389459":
  print "[FAIL]: centralizedadvertise returned different value than advertised."
