#pragma out Error opening source file 'testfile_repypp_example1.repy testfile_repypp_example2.repy'

"""
repypp.py is a preprocessor for repy. It includes dependent files as 
needed.This is used to help the programmer avoid the need to use 
import. They can instead use "include X" which works somewhat like 
"from X import *".

This script tests if repypp.py check erroneous include statements
(have multiple arguments).

"""

import os
import test_repypp_library

def main():
    filecontent1 = '''def foo1():
  pass
'''
    filecontent2 = '''def foo2():
  pass
'''
    filecontent3 = '''include testfile_repypp_example1.repy testfile_repypp_example2.repy
def bar():
  pass
'''
    #create a temporary_file1 contains:
    #def foo1():
    #  pass 
    test_repypp_library.createtempfile('testfile_repypp_example1.repy', filecontent1)

    #create a temporary_file2 contains:
    #def foo2():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example2.repy', filecontent2)

    #create a temporary_file3 contains:
    #include testfile_repypp_example1.repy testfile_repypp_example2.repy
    #def bar():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example3.repy', filecontent3)

    test_repypp_library.preprocess('testfile_repypp_example3.repy')

    if os.path.isfile('testfile_repypp_example3_preprocessed.repy'):
     os.remove('testfile_repypp_example3_preprocessed.repy')
    
    os.remove('testfile_repypp_example1.repy')
    os.remove('testfile_repypp_example2.repy')
    
if __name__ == "__main__":
  main()
