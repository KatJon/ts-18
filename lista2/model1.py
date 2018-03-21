import sys
import queue as q
import numpy as np
from random import (random)

class Model1:
    size = 0
    conn = None
    route = None
    use_smart = False

    def __init__(self, size):
        self.size = size
        self.conn = np.zeros((size, size))
        self.route = np.full((size, size), -1, dtype=int)

    def add(self, u, v, h):
        self.conn[u][v] = h
        self.conn[v][u] = h

        # we might get new shorter track
        for x in range(self.size):
            self.route[v][x] = -1
            self.route[x][u] = -1
            self.route[u][x] = -1
            self.route[x][v] = -1
            
    def connect(self, src, dest):
        v = src
        while v != dest:
            u = self.find_hop(v, dest)
            h = self.conn[v][u]
            roll = random()
            if roll > h:
                return False
            else:
                v = u
        return True

    def find_hop(self, src, dest):
        if src == dest:
            raise Exception("Already at the destination")
        if self.route[src][dest] < 0:
            _, prev = self.dijkstra(src)
            self.update_route(dest, prev)
        if self.route[src][dest] < 0:
            raise Exception("Not connected graph!!!")
        return self.route[src][dest]

    def update_route(self, dest, prev):
        v = dest
        while prev[v] != None:
            u = prev[v]
            self.route[u][dest] = v
            v = u 
        return

    def dijkstra(self, src):
        if self.use_smart:
            return self.smart_dijkstra(src)
        else:
            return self.classic_dijkstra(src)

    def classic_dijkstra(self, src):
        d = [1e100 for x in range(self.size)]
        d[src] = 0
        prev = [ None for _ in range(self.size)]
        Q = q.PriorityQueue()

        for i in range(self.size):
            item = (d[i], i)
            Q.put(item)

        while not Q.empty():
            _, u = Q.get()
            for v in range(self.size):
                if self.conn[u][v] > 0 and d[v] > d[u] + 1:
                    d[v] = d[u] + 1
                    prev[v] = u
                    Q.put((d[v], v))

        return d, prev

    def smart_dijkstra(self, src):
        d = [0 for x in range(self.size)]
        d[src] = 1
        prev = [ None for _ in range(self.size)]
        Q = q.PriorityQueue()

        for i in range(self.size):
            item = (1 - d[i], i)
            Q.put(item)

        while not Q.empty():
            _, u = Q.get()
            for v in range(self.size):
                h = self.conn[u][v]
                if h > 0 and d[v] < d[u] * h:
                    d[v] = d[u] * h
                    prev[v] = u
                    Q.put((1 - d[v], v))

        return d, prev