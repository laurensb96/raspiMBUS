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

mbus_rx = MBUS.MBUS()
mbus_tx = MBUS.MBUS()

while 1:
    # incoming TCP stream routine
    mbus_rx.tcp = conn.recv(BUFFER_SIZE)
    mbus_rx.decodeTCP()  # CAN bus data is extracted from the TCP stream

    # extract the relevant messages for direct processing
    if mbus_rx.cmd == 0x16:
        print('Switch accessory #:', mbus_rx.tcp[8], 'to state:', mbus_rx.tcp[9])
    if mbus_rx.cmd == 0x00 and mbus_rx.dlc == 8:
        print('Time =', mbus_rx.tcp[10], ':', mbus_rx.tcp[11], '(hr:min)')

    # assemble CAN message and transmit
    canMsgTx = can.Message(arbitration_id=int.from_bytes(mbus_rx.arb, byteorder='big'),
                         data=mbus_rx.can,
                         is_extended_id=True)
    bus.send(canMsgTx)

    # incoming CAN stream routine
    canMsgRx = bus.recv(0)
    if canMsgRx is not None:
        print(canMsgRx)
        mbus_tx.arb = canMsgRx.arbitration_id.to_bytes(4, 'big')
        mbus_tx.cmd = mbus_tx.arb[1]
        mbus_tx.dlc = canMsgRx.dlc
        mbus_tx.can = canMsgRx.data
        mbus_tx.encodeTCP()
        conn.send(mbus_tx.tcp)
conn.close()
