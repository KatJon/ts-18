#!/usr/bin/env python3
from Device import Device
from Cable import Cable

def main():
    L = 64
    cable = Cable(L)
    d_start = Device(cable, 0, 0.4, 'A')
    d_mid = Device(cable, L/2, 0.2, 'B')
    d_end = Device(cable, L-1, 0.3, 'C')

    for _ in range(100):
        cable.iteration()
        cable.print()
    pass
#end main

if __name__ == "__main__":
    main()