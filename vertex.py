#!/usr/bin/env python3

import numpy as np


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


class Geometric_Vertex(Vertex):
    def __init__(self, id, coordinates):
        super().__init__(id=id, neighbors=set())
        self.coordinates = tuple(coordinates)
        self.sector = 0

    def distance(self, u):
        d = 0
        for x_p, x_q in zip(self.coordinates, u.coordinates):
            d += (x_p - x_q) ** 2
        return d ** 0.5


class Contact_Vertex(Geometric_Vertex):
    def __init__(self, id, coordinates):
        super().__init__(id, coordinates)
        self.k = int(12.27 + np.random.randn(1) + 19.77)
