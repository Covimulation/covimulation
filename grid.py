#!/usr/bin/env python3

from collections import defaultdict


class Grid:
    def __init__(self, t, a=0, b=1):
        self.t = t
        self.a = a
        self.b = b
        self.sector = defaultdict(set)

    def assign_sector(self, u):
        sector = []
        side = (self.b - self.a) / self.t
        for x_i in u.coordinates:
            sector.append(int(x_i / side))
        u.sector = tuple(sector)
        self.sector[u.sector].add(u)

    def adjacent_sectors(self, sector, d):
        adjacent_sector = [x - d for x in sector]
        yield tuple(adjacent_sector)
        for x in range(1, 2 * d + 1):
            adjacent_sector[0] += 1
            yield tuple(adjacent_sector)
        for y in range(1, 2 * d + 1):
            adjacent_sector[1] += 1
            yield tuple(adjacent_sector)
        for x in range(1, 2 * d + 1):
            adjacent_sector[0] -= 1
            yield tuple(adjacent_sector)
        for y in range(1, 2 * d):
            adjacent_sector[1] -= 1
            yield tuple(adjacent_sector)

    def adjacent_nodes(self, u, d):
        vertices = set()
        for sector in self.adjacent_sectors(u.sector, d):
            vertices = vertices.union(self.sector[sector])
        return vertices
