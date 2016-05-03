# Copyright (C) 2005-2015 Splunk Inc. All Rights Reserved.
# The file contains the specification for all db connect modular inputs
# * mi_opcua - the moudular input that facilitates OPC UA Client against Kepware OPC Server.

[mi_win_opcua://default]

description = <value>
* Description for this opc client

connection = <value>
* Indicates the connection parameter to the opc server.

username = <value>
* Optional user name to login the opc server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* Password while username is set.
* Leave it empty when OPC server does not set up user authentication.

connection_timeout = <value>
* Indicates the connection timeout.
* Examples: 30

measures = <value>
* Indicates the wildcards of selected resources to collect.
* Examples: Objects:S*:~A*

metrics_spec = <value>
* Indicates the specification of metrics for displaying additional fields.
* Leave it empty when no specification is defined.

separator = <value>
* Separator symbol to identify the node level in the tree view.
* Leave it empty when use colon . as separator.

[mi_win_opcua_event://default]

description = <value>
* Description for this opc client

connection = <value>
* Indicates the connection parameter to the opc server.

username = <value>
* Optional user name to login the opc server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* Password while username is set.
* Leave it empty when OPC server does not set up user authentication.

connection_timeout = <value>
* Indicates the connection timeout.

collect_duration = <value>
* Indicates the collection duration in milliseconds.

[mi_win_uaserver2://default]

description = <value>
* Description for this ua server

serverpath = <value>
* The server path for this server.

namespace = <value>
* The namespace of the services.

serverport = <value>
* The port of the service server.

nodefile = <value>
* Json node structure file.

connection_timeout = <value>
* Connection timeout.

