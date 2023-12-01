#pragma out Error opening source file ''

"""
repypp.py is a preprocessor for repy. It includes dependent files as 
needed.This is used to help the programmer avoid the need to use 
import. They can instead use "include X" which works somewhat like 
"from X import *".

This script tests if repypp.py check erroneous include statements
(have no arguments at all).
"""

import os
import test_repypp_library

def main():
    filecontent = '''include 
def bar():
  pass
'''
    if os.path.isfile('testfile_repypp_example.repy'):
        os.remove('testfile_repypp_example.repy')
    #create a temporary_file contains:
    #include 
    #def bar():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example.repy', filecontent)

    test_repypp_library.preprocess('testfile_repypp_example.repy')
    
    if os.path.isfile('testfile_repypp_example_preprocessed.repy'):
        os.remove('testfile_repypp_example_preprocessed.repy')
    
    os.remove('testfile_repypp_example.repy')
    
if __name__ == "__main__":
  main()
