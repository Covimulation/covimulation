#!/usr/bin/env python3

import random
from vertex import Person
from contact_graph import Contact_Graph


class SIR_Graph(Contact_Graph):
    def __init__(self, n, p, p_initial, t=None, a=0, b=1):
        self.p = p
        self.p_initial = p_initial
        self.time = 0
        self.number_infected = 0
        self.infected = set()
        super().__init__(n, t, a, b)
        self.people = self.vertices
        print(self.number_infected, len(self.infected))

    def add_person(self, person):
        self.add_vertex(person)

    def create_vertex(self, id):
        coordinates = []
        for _ in range(2):
            coordinates.append(random.uniform(self.a, self.b))
        person = Person(id, coordinates)
        p = random.uniform(0, 1)
        if p <= self.p_initial:
            person.becomes_infected(self.time)
            self.infected.add(person)
            self.number_infected += 1
        self.add_person(person)

    def print_graph(self, increasing=True):
        if increasing:
            for person in sorted(self.people, key=lambda p: p.id):
                print(f"{person.id} - {person.status}")
                print("\t", end="")
                person.print_neighbors()
        else:
            for person in self.people:
                print(f"{person.id} - {person.status}")
                print("\t", end="")
                person.print_neighbors()

    def round(self):
        infected_this_round = set()
        for person in self.infected:
            for contact in person.neighbors:
                if contact.has_not_recovered():
                    p = random.uniform(0, 1)
                    if p <= self.p:
                        infected_this_round.add(contact)
        for contact in infected_this_round:
            self.infected.add(contact)
            contact.becomes_infected(self.time)
        self.number_infected = len(self.infected)
        self.time += 1

    def simulation(self, num_rounds, user_input=False):
        for _ in range(num_rounds):
            self.round()
            if user_input:
                x = input("Press 1 to print graph")
                if x == "1":
                    print(self.number_infected)
                    # self.print_graph()


def main():
    random.seed(1)
    G = SIR_Graph(n=10 ** 3, p=0.01, p_initial=0.01)
    # G.print_graph()
    G.simulation(5, True)
    # for v in sorted(list(G.vertices), key=lambda v: v.id):
    #     print(v.id)
    #     print(v.coordinates)
    #     v.print_neighbors(increasing=True)


if __name__ == "__main__":
    main()
