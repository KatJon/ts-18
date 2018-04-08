#!/usr/bin/env python3
import queue as q
import numpy as np
import random as rng
import networkx as nx
import matplotlib.pyplot as plt

PACKET_SIZE = 8

def draw_graph(G, Title, T, K):
    plt.figure(K)
    plt.suptitle(Title)
    plt.title("T = {0:.2%}".format(T))
    layout = nx.circular_layout(G)
    nx.draw_circular(G, with_labels=True)

def route(G, N, C, A, src, dest):
    d, prev = dijkstra(G, N, C, A, src, dest)
    payload = N[src][dest]
    cur_route = []
    v = dest
    while v != src and prev[v] != None:
        cur_route.append(v)
        p = prev[v]
        A[p][v] += payload
        A[v][p] += payload
        v = p
    cur_route.reverse()

def dijkstra(G, N, C, A, src, dest):
    d = [1e100 for x in range(10)]
    d[src] = 0
    prev = [ None for _ in range(10)]
    Q = q.PriorityQueue()

    for i in range(10):
        item = (d[i], i)
        Q.put(item)

    while not Q.empty():
        _, u = Q.get()
        for v in range(10):
            if (u,v) in G.edges() and d[v] > d[u] + 1:
                sumA = A[u][v] + N[u][v]
                newA = PACKET_SIZE * sumA
                if C[u][v] > newA:
                    d[v] = d[u] + 1
                    prev[v] = u
                    Q.put((d[v], v))

    return d, prev

def makeGraph():
    G = nx.Graph()
    G.add_nodes_from(range(10))
    edges = [
        (0,1), (0,2), (0,8),
        (1,5), (1,7),
        (2,3), (2,4),
        (3,9), (3,7),
        (4,5), (4,6),
        (5,9),
        (6,7), (6,8),
        (8,9)
    ]

    for edge in edges:
        u,v = edge
        G.add_edge(u,v)
    
    return G

def empty_matrix():
    return np.zeros((10,10), dtype=np.int32)

def N_matrix():
    N = empty_matrix()
    for i in range(10):
        for j in range(10):
            if i != j:
                N[i][j] = 64
    return N

def C_matrix(G):
    C = empty_matrix()
    for u,v in G.edges():
        bits = 512 * PACKET_SIZE
        C[u][v] = bits
        C[v][u] = bits
    return C

def A_matrix(G, N, C):
    A = empty_matrix()
    for i in range(10):
        for j in range(10):
            if i > j:
                route(G, N, C, A, i, j)
    return A

def calc_timeout(G, N, C, A):
    sum_N = 0
    sum_e = 0

    for i in range(10):
        for j in range(10):
            if i > j:
                sum_N += N[i][j]
    
    for u,v in G.edges():
        sum_e += A[u][v] / (C[u][v] / PACKET_SIZE - A[u][v])
    
    return sum_e/sum_N

def test_reliability(G, N, C, p, T_max):
    Reps = 10000
    K = 0
    for _ in range(Reps):
        copy = G.copy()
        for a, b in G.edges():
            roll = rng.random()
            if (roll > p):
                copy.remove_edge(a, b)
        
        if nx.is_connected(copy):
            A = A_matrix(G, N, C)
            print(A)
            T = calc_timeout(G, N, C, A)
            if T < T_max:
                K += 1

    return 100*K/Reps

if __name__ == "__main__":
    G = makeGraph()
    N = N_matrix()
    C = C_matrix(G)
    A = A_matrix(G, N, C)
    T = calc_timeout(G, N, C, A)

    T_max = 1.1 * T
    p = 0.9

    R = test_reliability(G, N, C, p, T_max)
    print("Reliability: {0:.2f}%".format(R))

    # draw_graph(G, "Petersen, bazowy", T, 1)
    # plt.show()