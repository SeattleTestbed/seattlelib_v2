#pragma out Invalid number of arguments
#pragma out repypp.py infile outfile

#pragma out preprocesses infile and includes content from the current directory.  Output is
#pragma out written to outfile.   Outfile and infile must be distinct.

"""
repypp.py is a preprocessor for repy. It includes dependent files as needed.This is used to help the 
programmer avoid the need to use import. They can instead use "include X" which works somewhat like "from X import *".

This script tests if repypp.py check erroneous arguments(have multiple arguments).

"""

import os
import sys
import tempfile
import subprocess

def main():
    #create a temporary_file1 contains:
    #def foo():
    #  pass
    temporary_file1 = open('testfile_repypp_example1.repy', 'w')
    temporary_file1.write('def foo():\n  pass\n') 
    temporary_file1.close()

    #create a temporary_file2 contains:
    #include testfile_repypp_example1.repy
    #def bar():
    #  pass
    temporary_file2 = open('testfile_repypp_example2.repy', 'w')
    temporary_file2.write('include testfile_repypp_example1.repy\ndef bar():\n  pass\n') 
    temporary_file2.close()

    subprocess.call(['python', 'repypp.py', 'testfile_repypp_example2.repy', 'testfile_repypp_example2_preprocessed.repy' , 'testfile_repypp_example2.repy'])   
    
    if os.path.isfile('testfile_repypp_example2_preprocessed.repy'):
        os.remove('testfile_repypp_example2_preprocessed.repy')
        
    os.remove('testfile_repypp_example1.repy')
    os.remove('testfile_repypp_example2.repy')
    
if __name__ == "__main__":
  main()
