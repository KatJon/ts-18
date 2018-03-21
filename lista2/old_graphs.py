import numpy as np

def ord(v1,v2):
    if v1 < v2:
        return v1,v2
    else:
        return v2,v1

class Edge:
    v1 = 0
    v2 = 0

    def __init__(self, v1, v2):
        m1,m2 = ord(v1,v2)
        self.v1 = m1
        self.v2 = m2

    def __str__(self):
        return "({0}~{1})".format(str(self.v1),str(self.v2))

class Graph:
    edges = []
    vertices = 0;

    def __init__(self, vertices):
        self.vertices = vertices

    def __str__(self):
        return "G(|V|={0}, E=[{1}])".format(self.vertices, self.print_edges())

    def print_edges(self):
        edgestr = map(str, self.edges)
        return",".join(edgestr)

    def add(self, v1, v2):
        self.edges.append(Edge(v1,v2))