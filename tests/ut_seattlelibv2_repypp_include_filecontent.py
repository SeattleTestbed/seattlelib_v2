"""
repypp.py is a preprocessor for repy. It includes dependent files as 
needed.This is used to help the programmer avoid the need to use 
import. They can instead use "include X" which works somewhat like 
"from X import *".

This script tests correct include statements(whether repypp.py 
incorrectly touched file contents).
"""

import os
import test_repypp_library

def main():
    filecontent1 = '''def foo():
  pass
'''
    filecontent2 = '''include testfile_repypp_example1.repy
def bar():
  pass
'''
    #create a temporary_file1 contains:
    #def foo():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example1.repy', filecontent1)

    #create a temporary_file2 contains:
    #include testfile_repypp_example1.repy
    #def bar():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example2.repy', filecontent2)
    
    test_repypp_library.preprocess('testfile_repypp_example2.repy')

    # check whether the file contents match what we expect.
    test_repypp_library.checkcontent('testfile_repypp_example2_preprocessed.repy')
    
    os.remove('testfile_repypp_example2_preprocessed.repy')
    os.remove('testfile_repypp_example1.repy')
    os.remove('testfile_repypp_example2.repy')

if __name__ == "__main__":
  main()
