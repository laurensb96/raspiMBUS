class MBUS:
    tcp = b''
    cmd = 0
    dlc = 0
    arb = b'\x00\x00\x00'
    can = b''

    def decodeTCP(self):
        self.arb = self.tcp[0:4]  # arbitration field = 0x00 + CMD + hash code
        self.cmd = self.tcp[1]
        self.dlc = self.tcp[4]
        self.can = self.tcp[5:5+self.dlc]

    def encodeTCP(self):
        self.tcp = self.arb + self.dlc.to_bytes(1, 'big') + self.can + b'\x00' * (8-self.dlc)
