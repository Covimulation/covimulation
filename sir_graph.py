#!/usr/bin/env python3

import random
from vertex import Person
from contact_graph import Contact_Graph
import sys


class SIR_Graph(Contact_Graph):
    def __init__(self, n, p, p_initial=None, recovery_time=14, t=None, a=0, b=1):
        self.p = p
        if p_initial is not None:
            self.p_initial = p_initial
        else:
            self.p_initial = 1 / n

        self.recovery_time = recovery_time
        self.current_time = 0

        self.number_suspectible = n
        self.number_infected = 0
        self.number_recovered = 0

        self.susceptible = set()
        self.infected = set()
        self.recovered = set()

        super().__init__(n, t, a, b)
        while self.number_infected == 0:
            for person in self.vertices:
                p = random.uniform(0, 1)
                if p <= self.p_initial:
                    person.becomes_infected(self.current_time)
                    self.infected.add(person)
                    self.susceptible.remove(person)
                    self.number_infected += 1
                    self.number_suspectible -= 1
        self.number_of_new_cases = [self.number_infected]

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
            self.number_suspectible -= 1
        else:
            self.susceptible.add(person)
        self.add_person(person)

    def round(self):
        infected_this_round = set()
        recovers_this_round = set()
        for person in self.infected:
            if self.current_time - person.infection_time >= self.recovery_time:
                recovers_this_round.add(person)
            for contact in person.neighbors:
                if self.transmission(person, contact):
                    infected_this_round.add(contact)
            if self.current_time - person.infection_time >= 5:
                person.quarantines()

        for contact in infected_this_round:
            self.infected.add(contact)
            self.number_infected += 1
            contact.becomes_infected(self.current_time)

            self.susceptible.remove(contact)
            self.number_suspectible -= 1

        for contact in recovers_this_round:
            contact.recovers()
            self.infected.remove(contact)
            self.number_infected -= 1
            self.recovered.add(contact)
            self.number_recovered += 1

        self.current_time += 1
        number_of_new_cases = len(infected_this_round)
        self.number_of_new_cases.append(number_of_new_cases)

    def transmission(self, A, B):
        if A.is_quarantined or B.is_quarantined:
            return False
        else:
            if B.is_susceptible():
                p = random.uniform(0, 1)
                return p <= self.p
            else:
                return False

    def simulation(self, num_rounds, output=False):
        if output:
            print(
                f"{'Round':^5} {'Number Susceptible': ^20} {'Number Infected': ^20} {'Number Recovered': ^20}"
            )
            print(
                f"{self.current_time: ^5} {self.number_suspectible: ^20} {self.number_infected: ^20} {self.number_recovered: ^20}"
            )
        for _ in range(num_rounds):
            self.round()
            if output:
                print(
                    f"{self.current_time: ^5} {self.number_suspectible: ^20} {self.number_infected: ^20} {self.number_recovered: ^20}"
                )


def growth_rate(number_of_new_cases, recovery_time=14):
    length = min(recovery_time, len(number_of_new_cases) - 1)
    total = 0
    for i in range(1, length):
        prev, curr = number_of_new_cases[i - 1], number_of_new_cases[i]
        if prev != 0:
            total += curr / prev
    return total / length


def infection_rate(target_growth_rate, n=10 ** 3, recovery_time=14, threshold=0.000001):
    actual_growth_rate = 0
    lower, upper = 0, 1
    while (
        abs(actual_growth_rate - target_growth_rate) > threshold
        and upper - lower > threshold
    ):
        # print(lower, upper, actual_growth_rate)
        p = (upper + lower) / 2
        G = SIR_Graph(n=n, p=p)
        G.simulation(recovery_time)
        actual_growth_rate = growth_rate(G.number_of_new_cases)
        if actual_growth_rate > target_growth_rate:
            upper = p
        else:
            lower = p
    return p


def main():
    if len(sys.argv) == 1:
        n = 10 ** 3
    else:
        n = int(sys.argv[1])
    target_growth_rate = 1.1
    p = 0
    for _ in range(10):
        p += infection_rate(target_growth_rate, n=n)
    p = p / 10
    print(f"Average infection rate: {p:0.05f}")


if __name__ == "__main__":
    main()