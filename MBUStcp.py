import MBUS

# create MBUS receive and transmit object instances
# receive side processes data incoming from TCP to CAN bus
# transmit side processes data incoming from CAN bus to TCP
mbus_dn = MBUS.MBUS()
mbus_up = MBUS.MBUS()
mbus_MFX = MBUS.MBUS()

while 1:
    # incoming TCP stream routine
    mbus_dn.rxTCP()

    # extract the relevant messages for direct processing
    if mbus_dn.cmd == 0x16:
        print('Switch accessory #:', mbus_dn.data[0:4], 'to position:', mbus_dn.data[4], 'to state:', mbus_dn.data[5])
    if mbus_dn.cmd == 0x00 and mbus_dn.dlc == 8:
        print('Time =', mbus_dn.data[5], ':', mbus_dn.data[6], '(hr:min)')

    # assemble CAN message, transmit and clear the buffer
    mbus_dn.txCAN()
    mbus_dn.clear()

    mbus_up.rxCAN(0)

    # do some processing

    # assemble TCP message, transmit and clear the buffer
    mbus_up.txTCP()
    mbus_up.clear()
conn.close()