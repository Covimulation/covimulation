#!/usr/bin/env python3

import random
from contact_distribution import world_pdf


class Vertex:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = set(neighbors)

    def add_neighbor(self, u):
        self.neighbors.add(u)

    def has_neighbor(self, u):
        return u in self.neighbors

    def print_neighbors(self, increasing=True):
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
    def __init__(self, id, coordinates, pdf):
        super().__init__(id, coordinates)
        self.k = pdf()


class Person(Contact_Vertex):
    def __init__(self, id, coordinates):
        super().__init__(id, coordinates, world_pdf)
        self.status = "S"
        self.asymptomatic = random.uniform(0, 1) <= 0.25
        self.is_quarantined = False

    def becomes_infected(self, time):
        self.infection_time = time
        self.status = "I"

    def recovers(self):
        self.status = "R"

    def quarantines(self):
        self.is_quarantined = True

    def is_symptomatic(self, time):
        return not self.asymptomatic and self.infection_time - time >= 5

    def is_infected(self):
        return self.status == "I"

    def has_recovered(self):
        return self.status == "R"

    def is_susceptible(self):
        return self.status == "S"

    def print_status(self):
        if self.status == "S":
            print("Suspectible")
        elif self.status == "I":
            print("Infected")
        elif self.status == "R":
            print("Recovered")
