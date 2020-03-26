import socket
import can

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, address = s.accept()
print('Connection address:', address)

bus = can.interface.Bus(bustype='kvaser', channel='0', bitrate=500000)

while 1:
    msg = conn.recv(BUFFER_SIZE)

    CMD = msg[1]
    can_arb = msg[1:4] # arbitration field = CMD + hash code
    DLC = msg[4]
    can_data = msg[5:5+DLC]

    if CMD == 0x16:
        print('Switch accessory #:', msg[8], 'to state:', msg[9])
    if CMD == 0x00 and DLC == 8:
        print('Time =', msg[10], ':', msg[11], '(hr:min)')
    canMsg = can.Message(arbitration_id=int.from_bytes(can_arb, byteorder='big'),
                         data=can_data,
                         is_extended_id=True)
    bus.send(canMsg)
conn.close()
