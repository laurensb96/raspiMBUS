import socket
import MBUS

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, address = s.accept()
print('Connection address:', address)


while 1:
    key = input()
    if key == 'k':
        break
    msg = MBUS.s88_event(int(key))
    conn.send(msg)
conn.close()
