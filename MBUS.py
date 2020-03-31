class MBUS:
    tcp = b''
    cmd = 0
    hash = b'\x00\x00'
    dlc = 0
    data = b''

    def decodeTCP(self):
        self.cmd = self.tcp[1]
        self.hash = self.tcp[2:4]
        self.dlc = self.tcp[4]
        self.data = self.tcp[5:5+self.dlc]

    # encode TCP stream with received CAN data, extending each data frame with zero bytes to length 8
    def encodeTCP(self):
        self.tcp = self.cmd.to_bytes(2, 'big') + self.hash + self.dlc.to_bytes(1, 'big') + self.data + b'\x00' * (8-self.dlc)
