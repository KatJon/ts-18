#!/usr/bin/env python3
import numpy as np
import random as rng
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, Title, K):
    plt.figure(K)
    plt.suptitle(Title)
    plt.title("T = {0:.2%}".format(0))
    layout = nx.circular_layout(G)
    nx.draw_circular(G, with_labels=True)
    edgeLabels = {}
    for a, b in G.edges():
        cap = G.get_edge_data(a, b, {"cap":0})["cap"]
        edgeLabels[(a, b)] = str(cap)
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edgeLabels, clip_on=False) # draw the edge labels


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
        n = rng.randint(4, 12) # max num of packets
        G.add_edge(u,v, capacity=2**n+1)
    
    return G

def empty_matrix():
    return np.zeros((10,10), dtype=np.int32)

def gen_flow():
    N = empty_matrix()
    for i in range(10):
        for j in range(10):
            if i > j:
                x = rng.randint(2, 128)
                N[i][j] = x
                N[j][i] = x
    return N

def sum_flow(N):
    sum = 0
    for i in range(10):
        for j in range(10):
            sum += N[i][j]
    return sum / 2

def get_cap(G):
    cap = empty_matrix()
    for a, b in G.edges():
        cap[a][b] = G.get_edge_data(a, b, {"capacity":0})["capacity"]
    return cap

if __name__ == "__main__":
    G = makeGraph()
    N = gen_flow()


    # draw_graph(G, "Petersen", 1)
    # plt.show()