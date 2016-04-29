import sys
import os
import subprocess

import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

SCHEME = """
<scheme>
    <title>OPC UA Pull Connect</title>
    <description>Manage the data collection from OPC UA Server.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>

    <endpoint>
        <args>

            <arg name="connection">
                <title>OPC Server Connection</title>
                <description> connection parameters to access OPC server.</description>
            </arg>

            <arg name="username">
                <title>OPC Server Login User</title>
                <description> Login User to access OPC server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="password">
                <title>OPC Server Login Password</title>
                <description> Login Password to access OPC server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="connection_timeout">
                <title>OPC Server Connection Timeout</title>
                <description> connection Timeout to access OPC server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="description">
                <title>Descrption</title>
                <description>Description for this data collector.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="measures">
                <title>Measure Setups</title>
                <description>Resources to collect from, can be wild cards.</description>
            </arg>

            <arg name="metrics_spec">
                <title>Metrics Specification</title>
                <description>Specification for metrics to display.</description>
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

def mi_opcua_py():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, "mi_opcua.py"))

if __name__ == '__main__':
    logger.info("---- opc ua ----")

    if len(sys.argv) > 1 and sys.argv[1] == "--scheme":
                do_scheme()
    else:
        logger.debug("Before launching python process to load data.")
        logger.debug("Python command : %s" % pycmd())
        logger.debug("Python service script: %s" % mi_opcua_py())
        try:
            ret = subprocess.call([pycmd(), mi_opcua_py()], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)
        except Exception as ex:
            logger.critical("Service call returns error: %s" % ex)
            
        logger.debug("End of data collection.")


'''
if __name__ == '__main__':
    logger.info("---- opc ua ----")
    
    if len(sys.argv) > 1:
        import mi_opcua as mi
        try:
            if sys.argv[1] == "--scheme":
                mi.do_scheme()
            elif sys.argv[1] == "--validate-arguments":
                mi.validate_arguments()
            elif sys.argv[1] == "--test":
                mi.test()
            else:
                mi.usage()
                
        except Exception as ex:
            logger.critical(ex)
    else:
        try:
            ret = subprocess.call([pycmd(), mi_opcua_py()], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)
        except Exception as ex:
            logger.critical(ex)

'''
