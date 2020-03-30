#!/usr/bin/env python3

import random
import math
from grid import Grid
from vertex import Contact_Vertex
from graph import Graph


class Contact_Graph(Graph):
    def __init__(self, n, t=None, a=0, b=1):
        super().__init__(vertices=set(), directed=False)
        self.a = a
        self.b = b
        self.size = 0
        self.t = t
        if t is None:
            self.t = int(math.sqrt(n / math.log(n)))
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
        v = Contact_Vertex(id, coordinates)
        self.add_vertex(v)

    def update_edges(self, u):
        i = 0
        while len(u.neighbors) < u.k:
            s = len(u.neighbors)
            new_nodes = self.Grid.adjacent_nodes(u, i)
            if s + len(new_nodes) > u.k:
                new_nodes = sorted(list(new_nodes), key=lambda v: u.distance(v))
                new_nodes = set(new_nodes[: u.k - s])
            u.neighbors = u.neighbors.union(self.Grid.adjacent_nodes(u, i))
            i += 1


def main():
    random.seed(1)
    G = Contact_Graph(n=10 ** 6)
    # for v in sorted(list(G.vertices), key=lambda v: v.id):
    #     print(v.id)
    #     print(v.coordinates)
    #     v.print_neighbors(increasing=True)


if __name__ == "__main__":
    main()
