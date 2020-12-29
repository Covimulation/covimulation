#!/usr/bin/env python3

import random
from numpy.random import lognormal
from numpy import exp, sqrt, log, rint
from collections import Counter
from matplotlib.pyplot import show, bar


def incubation_period(x=1.621, s=0.418):
    return lognormal(mean=x, sigma=s)


class Person:
    __slots__ = [
        "id",
        "coordinates",
        "contacts",
        "number_of_contacts",
        "status",
        "symptomatic",
        "is_quarantined",
        "group_number",
        "is_high_contact",
        "infection_time",
        "sector",
        "incubation_period",
    ]

    def __init__(
        self,
        id,
        coordinates,
        contact_distribution,
        asymptomatic_rate,
        number_of_groups=1,
    ):
        self.id = id
        self.coordinates = coordinates
        self.contacts = set()
        if contact_distribution is not None:
            self.number_of_contacts = contact_distribution()
        else:
            self.number_of_contacts = 0
        self.status = "S"
        self.symptomatic = random.uniform(0, 1) >= asymptomatic_rate
        self.is_quarantined = False
        self.group_number = random.randint(0, number_of_groups - 1)
        self.is_high_contact = False
        self.infection_time = None
        self.incubation_period = incubation_period()

    def add_contact(self, contact):
        self.contacts.add(contact)

    def distance(self, u):
        d = 0
        for x_p, x_q in zip(self.coordinates, u.coordinates):
            d += (x_p - x_q) ** 2
        return d ** 0.5

    def becomes_infected(self, time):
        self.infection_time = time
        self.status = "I"

    def recovers(self):
        self.status = "R"

    def quarantines(self):
        self.is_quarantined = True

    def unquarantines(self):
        self.is_quarantined = False

    def is_symptomatic(self, time):
        return (
            self.is_infected()
            and self.symptomatic
            and time - self.infection_time >= self.incubation_period
        )

    def is_contagious(self, time):
        return (
            self.is_infected()
            and time - self.infection_time >= self.incubation_period - 2
        )

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

    def high_contact(self, threshold):
        self.is_high_contact = self.number_of_contacts >= threshold


def main():
    f = incubation_period()
    hist = Counter()
    for _ in range(10 ** 3):
        hist[int(f())] += 1
    print(hist)
    bar(hist.keys(), hist.values())
    for key, value in hist.items():
        print(key, value)
    show()
    return 0


if __name__ == "__main__":
    main()
