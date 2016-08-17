"""
Demonstrate that Python's `from MODULE import *` hides names with 
an underscore prefix from the importer's namespace.
"""
from examplelib import *

try:
  _foo
except NameError:
  # The expected, correct exception.
  pass
else:
  print "Error! Expected examplelib's `_foo` to be hidden!"

