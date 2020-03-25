#!/usr/bin/env python3

import random
from graph import Vertex, Graph


def distance(p, q):
    d = 0
    for x_p, x_q in zip(p, q):
        d += (x_p - x_q) ** 2
    return d ** 0.5


class Geometric_Vertex(Vertex):
    def __init__(self, id, coordinates):
        super().__init__(id=id, neighbors=set())
        self.coordinates = tuple(coordinates)

    def distance(self, q):
        d = 0
        for x_p, x_q in zip(self.coordinates, q.coordinates):
            d += (x_p - x_q) ** 2
        return d ** 0.5


class Random_Geometric_Graph(Graph):
    def __init__(self, n, r, d=2, a=0, b=1):
        super().__init__(vertices=set(), directed=False)
        self.r = r
        self.d = d
        self.a = a
        self.b = b
        self.size = 0
        for i in range(n):
            self.create_vertex(i)

    def add_vertex(self, v):
        for u in self.vertices:
            if v.distance(u) <= self.r:
                u.add_neighbor(v)
                v.add_neighbor(u)
        self.vertices.add(v)
        self.size += 1

    def create_vertex(self, id):
        coordinates = []
        for _ in range(self.d):
            coordinates.append(random.uniform(self.a, self.b))
        v = Geometric_Vertex(id, coordinates)
        self.add_vertex(v)


def main():
    random.seed(a=1, version=2)
    G = Random_Geometric_Graph(n=10, r=0.3)
    for v in sorted(list(G.vertices), key=lambda v: v.id):
        print(v.id)
        print(v.coordinates)
        print(v.neighbors)
    print(G.size)


if __name__ == "__main__":
    main()
