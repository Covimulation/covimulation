#!/usr/bin/env python3


class Graph:
    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.directed = directed
        self.size = len(vertices)

    def add_vertex(self, u):
        for v in self.vertices:
            if u.has_neighbor(v):
                v.add_neighbor(u)
        self.vertices.add(u)
        self.size += 1

    def print_graph(self, increasing=True):
        if increasing:
            for vertex in sorted(self.vertices, key=lambda v: v.id):
                print(vertex.id)
                print("\t", end="")
                vertex.print_neighbors()
        else:
            for vertex in self.vertices:
                print(vertex.id)
                print("\t", end="")
                vertex.print_neighbors()
