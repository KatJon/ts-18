#!/usr/bin/env python3
from binascii import crc32
import sys

def crc(data):
    my_crc = bin(crc32(bytes(data, 'ascii')))[2:]    
    fill_crc = ('0'*32) + my_crc

    return fill_crc[-32:]

def stuff(idata, outfile):
    frame = '01111110'

    checksum = crc(idata)

    output = ''
    ones = 0
    for c in idata:
        if c == '1':
            ones += 1
        else:
            ones = 0
        output += c
        if ones == 5:
            ones = 0
            output += '0'

    odata = frame + output + frame + checksum

    with open(outfile, 'w') as out:
        out.write(odata)
# end stuff

def unstuff(idata, outfile):
    if len(idata) < 8 + 8 + 32:
        print('Invalid input format')
        return

    f1 = idata[0:8]
    content = idata[8:-40]
    f2 = idata[-40:-32]
    checksum = idata[-32:]

    frame = '01111110'
        
    if f1 != frame or f2 != frame:
        print('Invalid frame')
        return
    
    data = ''
    ones = 0
    for c in content:
        if ones == 5:
            ones = 0
            if c != '0':
                print('Invalid stuffing')
                return
        else:
            if c == '1':
                ones += 1
            else:
                ones = 0
            data += c
    
    checksum1 = crc(data)

    if checksum != checksum1:
        print('Invalid checksum')
        return

    with open(outfile, 'w') as out:
        out.write(data)

# end unstuff

def main():
    if len(sys.argv) < 4:
        print("Not enough arguments")
        return

    infile = sys.argv[2]
    outfile = sys.argv[3]

    with open(infile, 'r') as input:
        idata = input.read()
        if sys.argv[1] == '-e':
            stuff(idata, outfile)
        else:
            unstuff(idata, outfile)
# end main   
    

    

if __name__ == "__main__":
    main()

