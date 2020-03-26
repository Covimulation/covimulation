#!/usr/bin/env python3


class Vertex:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = set(neighbors)

    def add_neighbor(self, u):
        self.neighbors.add(u)

    def has_neighbor(self, u):
        return u in self.neighbors

    def print_neighbors(self, increasing=False):
        if increasing:
            print(sorted([u.id for u in self.neighbors]))
        else:
            print([u.id for u in self.neighbors])


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
