pragma out Error opening source file 'non_exist.repy'

"""
repypp.py is a preprocessor for repy. It includes dependent files as needed.This is used to help the 
programmer avoid the need to use import. They can instead use "include X" which works somewhat like "from X import *".

This script tests if repypp.py check erroneous #include statements(include non-existing files).
"""

import os
import sys
import subprocess

def main():
    #create a temporary_file contains:
    #def foo():
    #  pass
    temporary_file = open('testfile_repypp_example.repy', 'w')
    temporary_file.write('include non_exist.repy\ndef bar():\n  pass') 
    temporary_file.close()

    subprocess.call(['python', 'repypp.py', 'testfile_repypp_example.repy', 'testfile_repypp_example_preprocessed.repy']) 
      
    if os.path.isfile('testfile_repypp_example_preprocessed.repy'):
        os.remove('testfile_repypp_example_preprocessed.repy')
        
    if os.path.isfile('testfile_repypp_example.repy'):
        os.remove('testfile_repypp_example.repy')
    
if __name__ == "__main__":
  main()
