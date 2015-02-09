"""
ut_seattlelibv2_repypp_include.py -- -- This script tests correct #include statements

"""

import os
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

    subprocess.call(['python', 'repypp.py',temporary_file2.name, 'unittest.py'])
    os.remove('unittest.py')

if __name__ == "__main__":
  main()
