"""
Demonstrate how Python overrides variables when importing a library.
"""

def check_variable_contents(variable, checkstring):
  if variable != checkstring:
    print "Unexpected contents in variable:", variable, 
    print "(expected " + checkstring + ")"

import examplelib
check_variable_contents(examplelib.foo, "examplelib.py's foo")

# Override the variable locally
examplelib.foo = "local override"
check_variable_contents(examplelib.foo, "local override")

# Re-import the library. The override should be intact.
import examplelib
check_variable_contents(examplelib.foo, "local override")
