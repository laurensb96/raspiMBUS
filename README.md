# raspiMBUS
MBUS implementation for Raspberry PI using TCP

process structure:\
downlink: Rocrail server -> TCP -> MBUS python script -> CAN -> Marklin connector box\
uplink: Marklin connector box -> CAN -> MBUS python script -> TCP -> Rocrail server\
the MBUS script is therefore a bidirectional translator between TCP and CAN\
it can do some direct processing as well, for accessories and railroad feedback systems
