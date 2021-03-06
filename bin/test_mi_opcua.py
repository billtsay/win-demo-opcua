'''
Created on Jan 19, 2016

@author: btsay
'''

import logging
import os
os.environ["PBR_VERSION"] = "1.9.1"

import mock
from mock import patch
from StringIO import StringIO

import splunk_opcua.utils as utils

def setup_logging(app, level=logging.DEBUG):
    return logging.getLogger(app)


x = dict()
x["name"] = "test"
x["connection"] = "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"
x["connection_timeout"] = "30"
x["measures"] = "O*:W*04:T*:T*"


y = dict()
y["name"] = "test"
y["connection"] = "opc.tcp://localhost:53530/OPCUA/SimulationServer"
y["username"] = "bill"
y["password"] = "monday"
y["connection_timeout"] = "300"
y["measures"] = "O*:S*:S*"

z = dict()
z["name"] = "test"
z["connection"] = "opc.tcp://localhost:9988/splunk/uaserver2"
#z["connection"] = "opc.tcp://localhost:9988 -- urn:abc"
#z["username"] = "bill"
#z["password"] = "monday"
z["metrics_spec"] = "metrics2.json"
z["connection_timeout"] = "300"
z["measures"] = "O*:~Ser*"


k = dict()
k["name"] = "test"
k["connection"] = "opc.tcp://192.168.208.187:4845"
#z["connection"] = "opc.tcp://localhost:9988 -- urn:abc"
#z["username"] = "bill"
#z["password"] = "monday"
k["metrics_spec"] = "metrics2.json"
k["connection_timeout"] = "300"
k["measures"] = "O*.Ser*"
k["separator"] = "."

'''
import urlparse

print urlparse.urlparse(y["connection"])
'''

def get_configs():
    return k
    #return y


utils.setup_logging = mock.MagicMock(side_effect=setup_logging)

import mi_opcua
mi_opcua.get_config = mock.MagicMock(side_effect=get_configs)


def test_mi_opcua_run():
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
    mi_opcua.run()
        

if __name__ == '__main__':
    test_mi_opcua_run()