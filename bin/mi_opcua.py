'''
Created on Jan 12, 2016

@author: btsay
'''
#import os
#os.environ["SPLUNK_HOME"] = "/home/btsay/Documents/splunk/"

import logging
import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

import os
import uaserver as ua
import json
import sys
from collections import OrderedDict as odict

from opcua import Client
from splunk_opcua import mi
from splunk_opcua.ua import node

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

            <arg name="separator">
                <title>Node Tree Separator</title>
                <description>The separator symbol to identify node level in the tree view.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            
        </args>
    </endpoint>
</scheme>

"""


def do_scheme():
    print (SCHEME)

def usage():
    print ("usage: %s [--scheme|--validate-arguments]")
    utils.os_specific_sys_exit(2)
    
def test():
    pass
    
def validate_arguments():
    pass

def get_config():
    config_str = sys.stdin.read()
    return utils.get_config(config_str)


def collect_data(stanza, measure, spec={}):
    out = sys.stdout

    try:
        #obj = symbol.join(m)
        data = measure.get_data_value()
        evt = odict()  # use ordered dict to keep order of values.
        evt["stanza"] = stanza
        evt["collect_time"] = str(data.SourceTimestamp)
        evt["node_id"] = measure.nodeid.Identifier
        evt["measure"] = measure.get_display_name().Text
        evt["status"] = data.StatusCode.name
        evt["data_type"] = data.Value.VariantType.name
        
        '''
    :ivar Null:
    :ivar Boolean:
    :ivar SByte:
    :ivar Byte:
    :ivar Int16:
    :ivar UInt16:
    :ivar Int32:
    :ivar UInt32:
    :ivar Int64:
    :ivar UInt64:
    :ivar Float:
    :ivar Double:
    :ivar String:
    :ivar DateTime:
    :ivar Guid:
    :ivar ByteString:
    :ivar XmlElement:
    :ivar NodeId:
    :ivar ExpandedNodeId:
    :ivar StatusCode:
    :ivar QualifiedName:
    :ivar LocalizedText:
    :ivar ExtensionObject:
    :ivar DataValue:
    :ivar Variant:
    :ivar DiagnosticInfo:
        '''
        if evt["data_type"] in ["Float", "Double"]:
            evt["value"] = utils.format_float(data.Value.Value)
            logger.debug("The value collected is %s = %s" % (evt["measure"], evt["value"]))
            
        elif evt["data_type"] in ["Int64", "String", "DateTime", "Guid", "Int32", "UInt32", 
                                  "Boolean", "Int16", "UInt16", "UInt64", "StatusCode", 
                                  "LocalizedText", "ExpendedNodeId", "QualifiedName", "Byte", "SByte"]:
            evt["value"] = str(data.Value.Value)
            logger.debug("The value collected is %s = %s" % (evt["measure"], evt["value"]))
        else:
            logger.critical("Unable to convert the data value, the original value is %s=%s" % (evt["data_type"], data.Value.Value))   
            
        if spec.has_key(evt["measure"]):
            m = spec[evt["measure"]]
            evt["unit"] = m["unit"]
            evt["asset"] = m["asset"]
            evt["metric"] = m["metric"]
            if m.has_key("optimum"):
                evt["optimum"] = m["optimum"]
                
            evt["demo"] = "True"
        
        mi.print_kv_event(stanza, evt["collect_time"], evt, out)
        logger.debug("Collecting measure : %s" % evt["measure"])
    except Exception as ex:
        logger.critical(ex)

def run():
    logger.debug("Modular Input mi_opcua command: %s" % sys.argv)
    if len(sys.argv) > 1:
        try:
            if sys.argv[1] == "--scheme":
                do_scheme()
            elif sys.argv[1] == "--validate-arguments":
                validate_arguments()
            elif sys.argv[1] == "--test":
                test()
            else:
                usage()
        except Exception as ex:
            logger.critical(ex)
    else:
        logger.debug("Modular Input mi_opcua Starts data collection.")
        
        configs = get_config()
        logger.debug("Configuration: %s" % configs)
        stanza = configs["name"]
        SP = configs.get("separator", ":")
        patterns = configs["measures"].split(SP)
        tout = configs["connection_timeout"].strip()
        spec = configs.get("metrics_spec", "n.a.").strip()
        timeout = 1 if len(tout) <= 0 else int(tout)

        conn = configs["connection"]   ## "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"

        if configs.has_key("username"):
            username = configs["username"].strip()
            if len(username)>0:
                password = configs["password"].strip()
                conn = "%s?username=%s&password=%s" % (conn, username, password)
    
        client = Client(conn, timeout=timeout)

        mi.init_stream(sys.stdout)
        try:
            if logger.isEnabledFor(logging.DEBUG):
                try:
                    servers = client.connect_and_find_servers()
                    logger.debug("Servers are found: ")
                    for s in servers:
                        print s
                        logger.debug("\tServer: %s" % s)
                except:
                    pass
                
                try:    
                    nservers = client.connect_and_find_servers_on_network()
                    logger.debug("Network Servers are found: ")
                    for n in nservers:
                        logger.debug("\tNetwork Server: %s" % n)
                except:
                    pass
                
                endpoints = None
                try:
                    endpoints = client.connect_and_get_server_endpoints()
                    logger.debug("Server Endpoints are found: ")                    
                    for e in endpoints:
                        logger.debug("\tServer Endpoint: %s" % e.EndpointUrl)
                        logger.debug("\t\tServer Details: %s" % e)
                except:
                    pass
                
            try:
                logger.info("Start connecting OPC Server [%s]." % conn)
                client.connect()
                logger.info("OPC Server [%s] is connected." % conn)
            except Exception as ex:
                logger.error("Connecting to [%s] failed." % conn)
                if endpoints and len(endpoints)>0:
                    for ep in endpoints:
                        try:
                            conn = ep.EndpointUrl
                            logger.info("Try connect to another OPC Server [%s]." % conn)
                            client = Client(conn, timeout=timeout)
                            client.connect()
                            logger.info("OPC Server [%s] is connected." % conn)
                        except:
                            break
                else:
                    raise ex
                
            measures = []
            root = client.get_root_node()
            
            node.collect_measures(measures, patterns, root)
            
            md = {}
            try:
                jm = os.path.join(ua.data_dir(), spec)
                with open(jm, 'r') as mfp:
                    md = json.load(mfp)
                    mfp.close()
            except:
                pass

            for m in measures:
                collect_data(stanza, m[len(m)-1], spec=md)
                
        except Exception as ex:
            logger.critical(ex)
        finally:
            mi.fini_stream(sys.stdout)
            logger.info("---- end of opc ua ----")
            client.disconnect()

if __name__ == '__main__':
    logger.info("---- opc ua ----")
    try:
        run()
    except Exception as ex:
        logger.critical(ex)




