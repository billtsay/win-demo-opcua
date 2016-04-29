'''
Created on Jan 19, 2016

@author: btsay
'''
import os
import sys
import subprocess

def pycmd():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, os.pardir, "Python27", "python.exe"))

def test_mi_opcua_py():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, "test_mi_opcua.py"))

def test_mi_win_opcua_run():
    subprocess.call([pycmd(),  test_mi_opcua_py()], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)
    
    
     
        

if __name__ == '__main__':
    test_mi_win_opcua_run()