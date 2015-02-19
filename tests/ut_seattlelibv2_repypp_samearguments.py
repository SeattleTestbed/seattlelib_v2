#pragma out The infile and outfile must be different files

"""
repypp.py is a preprocessor for repy. It includes dependent files as 
needed.This is used to help the programmer avoid the need to use 
import. They can instead use "include X" which works somewhat like 
"from X import *".

This script tests if repypp.py check command line erroneous arguments
(have same arguments).

"""

import os
import subprocess
import sys
import test_repypp_library

def main():
    filecontent = '''def foo():
  pass
'''
    #create a temporary_file contains:
    #def foo():
    #  pass
    test_repypp_library.createtempfile('testfile_repypp_example.repy', filecontent)

    subprocess.call([sys.executable, 'repypp.py', 'testfile_repypp_example.repy', 'testfile_repypp_example.repy'])      
        
    os.remove('testfile_repypp_example.repy')
    
if __name__ == "__main__":
  main()
