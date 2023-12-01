#pragma out Invalid number of arguments
#pragma out repypp.py infile outfile

#pragma out preprocesses infile and includes content from the current directory.  Output is
#pragma out written to outfile.   Outfile and infile must be distinct.

"""
repypp.py is a preprocessor for repy. It includes dependent files as 
needed.This is used to help the programmer avoid the need to use 
import. They can instead use "include X" which works somewhat like 
"from X import *".

This script tests if repypp.py check command line erroneous arguments
(have no arguments at all).

"""

import subprocess
import sys

def main():
    try:
        subprocess.call([sys.executable, 'repypp.py'])  
    except:
        print 'Can not execute repypp.py'
    
if __name__ == "__main__":
  main()
