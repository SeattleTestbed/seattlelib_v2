#pragma out Invalid number of arguments
#pragma out repypp.py infile outfile

#pragma out preprocesses infile and includes content from the current directory.  Output is
#pragma out written to outfile.   Outfile and infile must be distinct.

"""
ut_seattlelibv2_repypp_multiplearguments.py -- This script tests if repypp.py check erroneous 
#include statements(have multiple arguments).

"""

import os
import sys
import tempfile
import subprocess

def main():
    #create a temporary_file1 contains:
    #def foo():
    # pass
    temporary_file1 = tempfile.NamedTemporaryFile(prefix='testfile_', suffix='.py', dir= os.path.dirname(os.path.realpath(__file__)), delete=True)
    temporary_file1.writelines(['def foo():\n','  pass'])

    #create a temporary_file2 contains:
    #include temporary_file1.py
    #def bar():
    # pass
    temporary_file2 = tempfile.NamedTemporaryFile(prefix='testfile_', suffix='.py', dir= os.path.dirname(os.path.realpath(__file__)), delete=True)
    temporary_file2.writelines(['include ' + temporary_file1.name + '\n','def bar():\n','  pass'])

    subprocess.call(['python', 'repypp.py', temporary_file2.name, 'unittest.py' , temporary_file1.name])   
    
    if os.path.isfile('unittest.py'):
        os.remove('unittest.py')
    
if __name__ == "__main__":
  main()
