"""
Demonstrate how Python overrides variables when importing a library.
"""

def check_variable_contents(variable, checkstring):
  if variable != checkstring:
    print "Unexpected contents in variable:", variable, 
    print "(expected " + checkstring + ")"

from examplelib import *
check_variable_contents(foo, "examplelib.py's foo")

# Override the variable locally
foo = "local override"
check_variable_contents(foo, "local override")

# Re-import the library. The variable contents should be reset.
from examplelib import *
check_variable_contents(foo, "examplelib.py's foo")
