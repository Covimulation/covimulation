#!/usr/bin/env python3


class Vertex:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = set(neighbors)

    def add_neighbor(self, vertex):
        self.neighbors.add(vertex.id)

    def has_neighbor(self, vertex):
        return vertex.id in self.neighbors


class Graph:
    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.directed = directed
        self.size = len(vertices)

    def add_vertex(self, v):
        for u in self.vertices:
            if v.has_neighbor(u):
                u.add_neighbor(v)
        self.vertices.add(v)
        self.size += 1
