import MBUS

# process structure:
# downlink: Rocrail server -> TCP -> MBUS python script -> CAN -> Marklin connector box
# uplink: Marklin connector box -> CAN -> MBUS python script -> TCP -> Rocrail server
# the MBUS script is therefore a bidirectional translator between TCP and CAN
# it can do some direct processing as well, for accessories and railroad feedback systems

# create MBUS down and up object instances
# down side processes data incoming from TCP to CAN bus
# up side processes data incoming from CAN bus to TCP
mbus_dn = MBUS.MBUS()
mbus_up = MBUS.MBUS()

while 1:
    # incoming TCP stream routine
    mbus_dn.rxTCP()

    # extract the relevant messages for direct processing
    if mbus_dn.cmd == 0x16:
        print('Switch accessory #:', mbus_dn.data[0:4], 'to position:', mbus_dn.data[4], 'to state:', mbus_dn.data[5])
    if mbus_dn.cmd == 0x00 and mbus_dn.dlc == 8:
        print('Time =', mbus_dn.data[5], ':', mbus_dn.data[6], '(hr:min)')
    if mbus_dn.cmd == 0x00 and mbus_dn.dlc == 5:
        print('Rocrail server shutdown')
        break

    # assemble CAN message, transmit and clear the buffer
    mbus_dn.txCAN()
    mbus_dn.clear()

    # incoming CAN stream routine, non-blocking
    mbus_up.rxCAN(0)

    # assemble TCP message, transmit and clear the buffer
    mbus_up.txTCP()
    mbus_up.clear()
MBUS.closeTCP()
MBUS.closeCAN()