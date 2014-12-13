def crc(msg, div, code):
    msg = list(msg)
    div = list(div)
    for i in range(len(msg)-len(code)):
        if msg[i] == '1':
            for j in range(len(div)):
                msg[i+j] = str((int(msg[i+j])+int(div[j]))%2)
    return ''.join(msg[-len(code):])
