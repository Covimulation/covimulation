#!/usr/bin/env python3

import random
import numpy as np
import math
from collections import defaultdict
from random_geometric_graph import Geometric_Vertex, Random_Geometric_Graph


class Contact_Vertex(Geometric_Vertex):
    def __init__(self, id, coordinates):
        super().__init__(id, coordinates)
        self.k = math.floor(12.27 + np.random.randn(1) + 19.77)


class Contact_Graph(Random_Geometric_Graph):
    def __init__(self, n, r, d=2, a=0, b=1):
        super().__init__(n, r, d, a, b)
        self.farthest_neighbor = defaultdict(float)

    def add_vertex(self, u):
        for v in self.vertices:
            if v.distance(u) <= self.r and :
                u.add_neighbor(v)
                v.add_neighbor(u)
        self.vertices.add(v)
        self.size += 1

    def create_vertex(self, id):
        coordinates = []
        for _ in range(self.d):
            coordinates.append(random.uniform(self.a, self.b))
        v = Contact_Vertex(id, coordinates)
        self.add_vertex(v)


def main():
    random.seed(1)
    G = Contact_Graph(n=10 ** 6, r=0.3)
    # for v in sorted(list(G.vertices), key=lambda v: v.id):
    #     print(v.id)
    #     print(v.coordinates)
    #     v.print_neighbors(increasing=True)


if __name__ == "__main__":
    main()
