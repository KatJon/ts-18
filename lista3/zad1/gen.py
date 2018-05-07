#!/usr/bin/env python3

from random import random

with open('data.in', 'w') as f:
    data = ''
    for i in range(512):
        data += '1' if random() > 0.5 else '0'
    
    f.write(data)
