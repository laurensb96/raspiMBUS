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

class MBUS:
    cmd = 0
    hash = b'\x00\x00'
    dlc = 0
    data = b''

    def rxTCP(self):
        tcp = conn.recv(BUFFER_SIZE)
        self.cmd = tcp[1]
        self.hash = tcp[2:4]
        self.dlc = tcp[4]
        self.data = tcp[5:5+self.dlc]

    def txTCP(self):
        tcp = self.cmd.to_bytes(2, 'big') + self.hash + self.dlc.to_bytes(1, 'big') + self.data + b'\x00' * (8-self.dlc)
        conn.send(tcp)

    def rxCAN(self,timeout):
        canMsgRx = bus.recv(timeout)
        if canMsgRx is not None:
            arb = canMsgRx.arbitration_id.to_bytes(4, 'big')
            self.cmd = arb[1]
            self.hash = arb[2:4]
            self.dlc = canMsgRx.dlc
            self.data = canMsgRx.data

    def txCAN(self):
        canMsgTx = can.Message(
            arbitration_id=int.from_bytes(self.cmd.to_bytes(2, 'big') + self.hash, byteorder='big'),
            data=self.data,
            is_extended_id=True)
        bus.send(canMsgTx)

    def clear(self):
        self.cmd = 0
        self.hash = b'\x00\x00'
        self.dlc = 0
        self.data = b''
