#!/usr/bin/env python3
from binascii import crc32
import sys

def crc(data):
    my_crc = bin(crc32(bytes(data, 'ascii')))[2:]    
    fill_crc = ('0'*32) + my_crc

    return fill_crc[-32:]
#end crc

def frame(data):
    flag = '01111110'
    checksum = crc(data)
    output = ''
    ones = 0
    for c in data:
        ones = ones + 1 if c == '1' else 0
        output += c
        if ones == 5:
            ones = 0
            output += '0'

    return flag + output + flag + checksum
#end frame

def encode(idata, outfile):
    odata = frame(idata)
    with open(outfile, 'w') as out:
        out.write(odata)
# end encode

def unframe(data):
    f1 = data[0:8]
    content = data[8:-40]
    f2 = data[-40:-32]
    checksum = data[-32:]

    flag = '01111110'
        
    if f1 != flag or f2 != flag:
        print('Invalid flag')
        return None

    data = ''
    ones = 0
    for c in content:
        if ones == 5:
            ones = 0
            if c != '0':
                print('Invalid stuffing')
                return None
        else:
            ones = ones + 1 if c == '1' else 0
            data += c
    
    checksum1 = crc(data)

    if checksum != checksum1:
        print('Invalid checksum')
        return None
    
    return data
#end unframe

def decode(idata, outfile):
    if len(idata) < 8 + 8 + 32:
        print('Invalid input format')
        return
    
    data = unframe(idata)

    if data == None:
        print('Error during reading frame')
        return

    with open(outfile, 'w') as out:
        out.write(data)
# end decode

def main():
    if len(sys.argv) < 4:
        print("Not enough arguments")
        return

    infile = sys.argv[2]
    outfile = sys.argv[3]

    with open(infile, 'r') as input:
        idata = input.read()
        if sys.argv[1] == '-e':
            encode(idata, outfile)
        else:
            decode(idata, outfile)
# end main   
    
if __name__ == "__main__":
    main()
