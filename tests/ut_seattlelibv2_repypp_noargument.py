#pragma out Invalid number of arguments
#pragma out repypp.py infile outfile

#pragma out preprocesses infile and includes content from the current directory.  Output is
#pragma out written to outfile.   Outfile and infile must be distinct.

"""
repypp.py is a preprocessor for repy. It includes dependent files as needed.This is used to help the 
programmer avoid the need to use import. They can instead use "include X" which works somewhat like "from X import *".

This script tests if repypp.py check erroneous arguments(have no arguments at all).

"""

import sys
import subprocess

def main():
    subprocess.call(['python', 'repypp.py'])   
    
    
if __name__ == "__main__":
  main()
