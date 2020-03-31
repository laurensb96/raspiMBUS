import socket
import can
import MBUS

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, address = s.accept()
print('Connection address:', address)

bus = can.interface.Bus(bustype='kvaser', channel='0', bitrate=500000)

# create MBUS receive and transmit object instances
# receive side processes data incoming from TCP to CAN bus
# transmit side processes data incoming from CAN bus to TCP
mbus_dn = MBUS.MBUS()
mbus_up = MBUS.MBUS()

def canTX(cmd,hash,data):
    canMsgTx = can.Message(
        arbitration_id=int.from_bytes(cmd.to_bytes(2, 'big') + hash, byteorder='big'),
        data=data,
        is_extended_id=True)
    bus.send(canMsgTx)

def programMFX():
    print('Program MFX loks')
    # first do lok discovery
    canMsgTx = can.Message(arbitration_id=int.from_bytes(0x02.to_bytes(2, 'big') + mbus_dn.hash, byteorder='big'),
                         data=[0x20],
                         is_extended_id=True)
    bus.send(canMsgTx)

    canMsgRx = bus.recv()
    arb = canMsgRx.arbitration_id.to_bytes(4, 'big')
    cmd = arb[1]
    dlc = canMsgRx.dlc
    data = canMsgRx.data
    if cmd == 0x03 and dlc == 5:
        print('Lok found with MFX-UID:', data[0:4], 'range =', data[4])
    # now bind an SID to the MFX-UID
    canMsgTx = can.Message(arbitration_id=int.from_bytes(0x04.to_bytes(2, 'big') + mbus_dn.hash, byteorder='big'),
                           data=data[0:4] + 0x02.to_bytes(2, 'big'),
                           is_extended_id=True)
    bus.send(canMsgTx)


while 1:
    # incoming TCP stream routine
    mbus_dn.tcp = conn.recv(BUFFER_SIZE)
    mbus_dn.decodeTCP()  # CAN bus data is extracted from the TCP stream

    # extract the relevant messages for direct processing
    if mbus_dn.cmd == 0x16:
        print('Switch accessory #:', mbus_dn.data[0:4], 'to position:', mbus_dn.data[4], 'to state:', mbus_dn.data[5])
    if mbus_dn.cmd == 0x16 and mbus_dn.data[3] == 0x33:
        programMFX()
    if mbus_dn.cmd == 0x00 and mbus_dn.dlc == 8:
        print('Time =', mbus_dn.data[5], ':', mbus_dn.data[6], '(hr:min)')

    # assemble CAN message and transmit
    canTX(mbus_dn.cmd, mbus_dn.hash, mbus_dn.data)

    # incoming CAN stream routine
    canMsgRx = bus.recv(0)
    if canMsgRx is not None:
        print(canMsgRx)
        arb = canMsgRx.arbitration_id.to_bytes(4, 'big')
        mbus_up.cmd = arb[1]
        mbus_up.hash = arb[2:4]
        mbus_up.dlc = canMsgRx.dlc
        mbus_up.data = canMsgRx.data
        mbus_up.encodeTCP()
        conn.send(mbus_up.tcp)
conn.close()