"""
repypp.py is a preprocessor for repy. It includes dependent files as needed.This is used to help the 
programmer avoid the need to use import. They can instead use "include X" which works somewhat like "from X import *".

This script tests correct #include statements
"""

import os
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

    subprocess.call(['python', 'repypp.py', 'testfile_repypp_example2.repy', 'testfile_repypp_example2_preprocessed.repy',])

    # check whether the file contents match what we expect.
    correctresult1 = 'def foo():\n  pass\n'
    correctresult2 = 'def bar():\n  pass\n'
    
    f = open('testfile_repypp_example2_preprocessed.repy','r')

    if not correctresult1 in f.read() and not correctresult2 in f.read():
        print "the result of repypp.py produces is not correct!"

    os.remove('testfile_repypp_example2_preprocessed.repy')
    os.remove('testfile_repypp_example1.repy')
    os.remove('testfile_repypp_example2.repy')

if __name__ == "__main__":
  main()
