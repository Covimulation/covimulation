#!/usr/bin/env python3

import random


class Person:
    def __init__(self, id, coordinates, contact_distribution):
        self.id = id
        self.coordinates = coordinates
        self.contacts = set()
        if contact_distribution is not None:
            self.number_of_contacts = contact_distribution()
        else:
            self.number_of_contacts = 0
        self.status = "S"
        self.symptomatic = random.uniform(0, 1) >= 0.25
        self.is_quarantined = False
        self.group_number = random.randint(0, 6)
        self.is_high_contact = False

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
        return self.symptomatic and time - self.infection_time > 5

    def is_contagious(self, time):
        return self.is_infected() and time - self.infection_time > 2

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
