#pragma out Error opening source file 'testfile_repypp_example1.repy testfile_repypp_example2.repy'
"""
repypp.py is a preprocessor for repy. It includes dependent files as needed.This is used to help the 
programmer avoid the need to use import. They can instead use "include X" which works somewhat like "from X import *".

This script tests if repypp.py check erroneous #include statements(have multiple arguments).

"""

import os
import sys
import subprocess

def main():
    #create a temporary_file1 contains:
    #def foo1():
    #  pass 
    temporary_file1 = open('testfile_repypp_example1.repy', 'w')
    temporary_file1.write('def foo1():\n  pass\n') 
    temporary_file1.close()

    #create a temporary_file2 contains:
    #def foo2():
    #  pass
    temporary_file2 = open('testfile_repypp_example2.repy', 'w')
    temporary_file2.write('def foo2():\n  pass\n') 
    temporary_file2.close()

    #create a temporary_file2 contains:
    #include testfile_repypp_example1.repy testfile_repypp_example2.repy
    #def bar():
    #  pass
    temporary_file3 = open('testfile_repypp_example3.repy', 'w')
    temporary_file3.write('include testfile_repypp_example1.repy testfile_repypp_example2.repy\ndef bar():\n  pass\n') 
    temporary_file3.close()

    subprocess.call(['python', 'repypp.py', 'testfile_repypp_example3.repy', 'testfile_repypp_example3_preprocessed.repy']) 

    if os.path.isfile('testfile_repypp_example3_preprocessed.repy'):
     os.remove('testfile_repypp_example3_preprocessed.repy')
    
    os.remove('testfile_repypp_example1.repy')
    os.remove('testfile_repypp_example2.repy')
    
if __name__ == "__main__":
  main()
