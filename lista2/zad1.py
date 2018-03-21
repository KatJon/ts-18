#!/usr/bin/env python3
import numpy as np
import random as rng

from model1 import *

N = 100000

def test_model(model, name):
    K = 0
    for i in range(N):
        src = rng.randint(0, model.size-1)
        dest = rng.randint(0, model.size-1)
        connected = model.connect(src, dest)
        K = K + 1 if connected else K
    
    print("{0} => Success: {1}, Sent: {2}, Ratio: {3}%".format(name, K, N, 100*K/N))

if __name__ == "__main__":
    SIZE = 20

    net1 = Model1(SIZE)
    for i in range(0, SIZE-1):
        net1.add(i, i+1, 0.95)

    net1.use_smart = False
    test_model(net1, "Model 1 Classic")
    net1.use_smart = True
    test_model(net1, "Model 1 Smart")

    net1.add(19, 0, 0.95)

    net1.use_smart = False
    test_model(net1, "Model 2 Classic")
    net1.use_smart = True
    test_model(net1, "Model 2 Smart")

    net1.add(0, 9, 0.8)
    net1.add(4, 14, 0.7)

    net1.use_smart = False
    test_model(net1, "Model 3 Classic")
    net1.use_smart = True
    test_model(net1, "Model 3 Smart")

    added = 0
    while added < 4:
        u = rng.randint(0, net1.size-1)
        v = rng.randint(0, net1.size-1)
        if net1.conn[u][v] == 0:
            net1.add(u, v, 0.4)
            added += 1
    
    net1.use_smart = False
    test_model(net1, "Model 4 Classic")
    net1.use_smart = True
    test_model(net1, "Model 4 Smart")

    # net2 = Model1(SIZE)
    # for i in range(4*SIZE):
    #     u = rng.randint(0, net2.size-1)
    #     v = rng.randint(0, net2.size-1)
    #     net2.add(u, v, rng.random())
    
    # net2.use_smart = False
    # test_model(net2, "Random Classic")
    # net2.use_smart = True
    # test_model(net2, "Random Smart")
