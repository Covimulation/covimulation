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
