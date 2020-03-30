#!/usr/bin/env python3

import random
from vertex import Person
from contact_graph import Contact_Graph


class SIR_Graph(Contact_Graph):
    def __init__(self, n, p, p_initial, recovery_time=14, t=None, a=0, b=1):
        self.p = p
        self.p_initial = p_initial

        self.recovery_time = recovery_time
        self.current_time = 0

        self.number_infected = 0
        self.number_recovered = 0

        self.infected = set()
        self.recovered = set()
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
            person.becomes_infected(self.current_time)
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
        recovers_this_round = set()
        for person in self.infected:
            for contact in person.neighbors:
                if contact.is_susceptible():
                    p = random.uniform(0, 1)
                    if p <= self.p:
                        infected_this_round.add(contact)
            if self.current_time - person.infection_time >= self.recovery_time:
                recovers_this_round.add(person)

        for contact in infected_this_round:
            self.infected.add(contact)
            self.number_infected += 1
            contact.becomes_infected(self.current_time)

        for contact in recovers_this_round:
            contact.recovers()
            self.infected.remove(contact)
            self.number_infected -= 1
            self.recovered.add(contact)
            self.number_recovered += 1

        self.number_infected = len(self.infected)
        self.current_time += 1

    def simulation(self, num_rounds):
        print(f"{'Round':^5} {'Number Infected': ^20} {'Number Recovered': ^20}")
        print(
            f"{self.current_time:^5} {self.number_infected: ^20} {self.number_recovered: ^20}"
        )
        for _ in range(num_rounds):
            self.round()
            print(
                f"{self.current_time:^5} {self.number_infected: ^20} {self.number_recovered: ^20}"
            )


def main():
    G = SIR_Graph(n=10 ** 3, p=0.01, p_initial=0.01)
    # G.print_graph()
    G.simulation(16)
    # for v in sorted(list(G.vertices), key=lambda v: v.id):
    #     print(v.id)
    #     print(v.coordinates)
    #     v.print_neighbors(increasing=True)


if __name__ == "__main__":
    main()
