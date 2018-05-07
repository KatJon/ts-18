#!/usr/bin/env python3
from Cable import Cable, Collision
from random import random, randint
from time import sleep

PACKET_SIZE = 40
P = 0.1
LENGTH = 80


class Device:
    def __init__(self, empty, push, msg, P):
        self.empty = empty
        self.push = push
        self.msg = msg
        self.P = P

        self.wait = 0
        self.sent = 0
        self.rem = 0
        self.coll = 0

    def tick(self):
        if self.rem > 0:
            self.push(self.msg)
            self.rem -= 1
            self.sent += 1
        elif self.sent > 0:
            return
        elif self.wait == 0:
            if self.empty and random() < P:
                self.push(self.msg)
                self.rem = PACKET_SIZE - 1
                self.sent = 1
        else:
            self.wait -= 1
    
    def collision(self):
        self.rem = 0
        self.coll += 1
        self.sent = 0
        if self.coll < 10:
            self.wait = randint(1, 2**self.coll)
        else:
            print('Cannot send ' + self.msg)
            self.coll = 0
            self.wait = 0

    def delivered(self):
        self.sent -= 1
        if self.sent == 0:
            self.coll = 0
            print('Delivered: ' + self.msg)

if __name__ == "__main__":
    cable = Cable(LENGTH)

    left_dev = Device(cable.emptyL, cable.pushL, '>', P)
    right_dev = Device(cable.emptyR, cable.pushR, '<', P)

    while(True):
        try:
            left_dev.tick()
            right_dev.tick()

            print(cable)
            L,R = cable.tick()

            if L:
                right_dev.delivered()
            
            if R:
                left_dev.delivered()

            sleep(0.03)
        except Collision:
            print('Collision')
            cable.clear()
            left_dev.collision()
            right_dev.collision()
        
