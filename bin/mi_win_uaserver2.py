import os
import sys
import subprocess

import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

SCHEME = """
<scheme>
    <title>UA Simulator Server II</title>
    <description>OPC UA Server Simulator II.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>

    <endpoint>
        <args>

            <arg name="serverpath">
                <title>UA Server path</title>
                <description>OPC UA server path.</description>
            </arg>

            <arg name="namespace">
                <title>UA Service Namespace</title>
                <description>OPC UA service Namespace.</description>
            </arg>

            <arg name="description">
                <title>Description</title>
                <description>The server description of the UA Server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="serverport">
                <title>UA Server port</title>
                <description>UA Server Port.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="nodefile">
                <title>Node Structure</title>
                <description> Node Structure JSON file.</description>
            </arg>

            <arg name="connection_timeout">
                <title>UA Server Connection Timeout</title>
                <description> connection Timeout to access UA server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            
        </args>
    </endpoint>
</scheme>

"""

def do_scheme():
    print (SCHEME)

def pycmd():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, os.pardir, "Python27", "python.exe"))

def mi_uaserver2_py():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, "mi_uaserver2.py"))


if __name__ == '__main__':
    logger.info("---- opc ua server ----")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--scheme":
        do_scheme()
    else:
        try:
            ret = subprocess.call([pycmd(), mi_uaserver2_py()], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)
        except Exception as ex:
            logger.critical(ex)
