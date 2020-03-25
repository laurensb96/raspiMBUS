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
    print(msg)
    can_arb = (msg[1] << 16) + (msg[2] << 8) + msg[3]
    DLC = msg[4]
    can_data = msg[5:5+DLC]
    canMsg = can.Message(arbitration_id=can_arb,
                         data=can_data,
                         is_extended_id=True)
    bus.send(canMsg)
conn.close()
