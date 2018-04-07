#!/usr/bin/env python3
import random as rng
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, T, R, K):
    plt.figure(K)
    plt.suptitle(T)
    plt.title("R = {0:.2%}".format(R))
    layout = nx.circular_layout(G)
    nx.draw_circular(G, with_labels=True)
    edgeLabels = {}
    for a, b in G.edges():
        weight = G.get_edge_data(a, b, {"weight":0})["weight"]
        edgeLabels[(a, b)] = str(weight)
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edgeLabels, clip_on=False) # draw the edge labels

def test_connectivity(G):
    N = 10000
    K = 0
    for _ in range(N):
        copy = G.copy()
        for a, b in G.edges():
            H = G.get_edge_data(a, b, {"weight":0})["weight"]
            roll = rng.random()
            if (roll > H):
                copy.remove_edge(a, b)
        
        if nx.is_connected(copy):
            K += 1
    
    return K/N

if __name__ == "__main__":
    G = nx.Graph()
    G.add_nodes_from(range(1, 21))

    for i in range(1,20):
        G.add_edge(i, i+1, weight=0.95)
    ratio = test_connectivity(G)
    title = "Zad 1.1"
    draw_graph(G, title, ratio, 1)

    G.add_edge(1, 20, weight=0.95)
    ratio = test_connectivity(G)
    title = "Zad 1.2"
    draw_graph(G, title, ratio, 2)

    G.add_edge(1, 10, weight=0.8)
    G.add_edge(5, 15, weight=0.7)
    ratio = test_connectivity(G)
    title = "Zad 1.3"
    draw_graph(G, title, ratio, 3)

    for i in range(4):
        u,v = rng.choice(list(nx.non_edges(G)))
        G.add_edge(u, v, weight=0.4)

    ratio = test_connectivity(G)
    title = "Zad 1.4"
    draw_graph(G, title, ratio, 4)

    plt.show()