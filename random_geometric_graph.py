#!/usr/bin/env python3

import random
from vertex import Geometric_Vertex
from graph import Graph
from grid import Grid


class Random_Geometric_Graph(Graph):
    def __init__(self, n, r, t=None, a=0, b=1):
        super().__init__(vertices=set(), directed=False)
        self.r = r
        self.a = a
        self.b = b
        self.size = 0
        self.t = t
        if t is None:
            self.t = int(2 * (b - a) / r)
        self.Grid = Grid(self.t, a)
        for i in range(n):
            self.create_vertex(i)
        for u in self.vertices:
            self.update_edges(u)

    def add_vertex(self, u):
        self.vertices.add(u)
        self.Grid.assign_sector(u)
        self.size += 1

    def create_vertex(self, id):
        coordinates = []
        for _ in range(2):
            coordinates.append(random.uniform(self.a, self.b))
        v = Geometric_Vertex(id, coordinates)
        self.add_vertex(v)

    def update_edges(self, u):
        d = (self.b - self.a) / self.t
        i = 0
        while d * i < self.r:
            new_nodes = self.Grid.adjacent_nodes(u, i)
            u.neighbors = u.neighbors.union(new_nodes)
            i += 1
        for v in self.Grid.adjacent_nodes(u, i):
            if u.distance(v) <= self.r:
                u.neighbors.add(v)


def main():
    random.seed(1)
    G = Random_Geometric_Graph(n=10 ** 6, r=0.05)
    # for v in sorted(list(G.vertices), key=lambda v: v.id):
    #     print(v.id)
    #     print(v.coordinates)
    #     v.print_neighbors(increasing=True)


if __name__ == "__main__":
    main()
