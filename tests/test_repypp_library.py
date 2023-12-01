'''
This script is a library for unit tests of repypp.py. It includes 
three functions: create a temporary file, execute repypp.py and 
check preprocessed file.
'''
import os
import sys
import subprocess

def createtempfile(filename, content):
    if os.path.isfile(filename):
        os.remove(filename)
    temporary_file = open(filename, 'w')
    temporary_file.write(content) 
    temporary_file.close()


def preprocess(filename):
    try:
        subprocess.call([sys.executable, 'repypp.py', filename, os.path.splitext(filename)[0] + '_preprocessed.repy'])
    except:
        print 'Can not execute repypp.py'

def checkcontent(filename):
    correctresult1 ='''def foo():
  pass
'''
    correctresult2 ='''def bar():
  pass
'''    
    f = open(filename,'r')

    if not correctresult1 in f.read() and not correctresult2 in f.read():
        print "the result of repypp.py produces is not correct!"
