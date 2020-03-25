S88_HEADER = b'\x00\x21\x47\x74\x07\x00\x00\x00\x00\x00\x00'


def s88_event(channel):
    msg = S88_HEADER + channel.to_bytes(2, 'big')
    print(msg)
    print(hex(msg[1]))
    if hex(msg[1]) == '0x21':
        print('S88 command')
    return msg
