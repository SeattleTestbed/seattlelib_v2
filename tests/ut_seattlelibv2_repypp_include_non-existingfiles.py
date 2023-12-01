#pragma out Error opening source file 'non_exist.repy'

"""
repypp.py is a preprocessor for repy. It includes dependent files as 
needed.This is used to help the programmer avoid the need to use 
import. They can instead use "include X" which works somewhat like 
"from X import *".

This script tests if repypp.py check erroneous include statements
(include non-existing files).
"""

import os
import test_repypp_library

def main():
    filecontent = '''include non_exist.repy
def bar():
  pass
'''
    #create a temporary_file contains:
    #include non_exist.repy
    #def bar():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example.repy', filecontent)

    if os.path.isfile('non_exist.repy'):
        os.remove('non_exist.repy')

    test_repypp_library.preprocess('testfile_repypp_example.repy')

    if os.path.isfile('testfile_repypp_example_preprocessed.repy'):
        os.remove('testfile_repypp_example_preprocessed.repy')
        
    if os.path.isfile('testfile_repypp_example.repy'):
        os.remove('testfile_repypp_example.repy')
    
if __name__ == "__main__":
  main()
