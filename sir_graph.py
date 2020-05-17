#!/usr/bin/env python3

import random
from person import Person
from contact_graph import Contact_Graph
import sys
import os
from contact_distribution import world_pdf
from multiprocessing import Process


class SIR_Graph(Contact_Graph):
    def __init__(
        self,
        p,
        contact_distribution,
        n=0,
        file_name=None,
        p_initial=None,
        initial_infected=1,
        recovery_time=14,
        t=None,
        a=0,
        b=1,
        mechanism=None,
        quarantine_probability=0,
        number_of_groups=1,
        contact_threshold=0,
    ):
        super().__init__(
            contact_distribution=contact_distribution,
            n=n,
            file_name=file_name,
            t=t,
            a=a,
            b=b,
            number_of_groups=number_of_groups,
        )
        self.p = p
        if p_initial is not None:
            self.p_initial = p_initial
        else:
            self.index_patients = set(
                random.sample(list(range(self.size)), k=initial_infected)
            )

        self.recovery_time = recovery_time
        self.quarantine_probability = quarantine_probability
        self.contact_threshold = contact_threshold
        self.random_quarantine = mechanism == "random quarantine"
        self.scheduled_quarantine = mechanism == "scheduled quarantine"
        self.symptomatic_quarantine = mechanism in {
            "symptomatic quarantine",
            "scheduled quarantine",
        }

        self.high_contact_targeting = mechanism == "high-contact targeting"

        self.current_time = 0

        self.number_suspectible = n
        self.number_infected = 0
        self.number_recovered = 0

        self.susceptible = set([person for person in self.people])
        self.infected = set()
        self.recovered = set()

        if self.scheduled_quarantine:
            self.groups = [set() for _ in range(self.number_of_groups)]

        while self.number_infected == 0:
            for person in self.people:
                infected = False
                if p_initial is not None:
                    infected = random.uniform(0, 1) <= self.p_initial
                else:
                    infected = person.id in self.index_patients
                if infected:
                    person.becomes_infected(self.current_time)
                    self.infected.add(person)
                    self.susceptible.remove(person)
                    self.number_infected += 1
                    self.number_suspectible -= 1

        if self.random_quarantine:
            for person in self.people:
                if random.uniform(0, 1) <= self.quarantine_probability:
                    person.quarantines()

        if self.scheduled_quarantine:
            for person in self.people:
                self.groups[person.group_number].add(person)
                person.quarantines()

        self.number_of_new_cases = [self.number_infected]

    def round(self):
        if self.scheduled_quarantine:
            group_number = self.current_time % self.number_of_groups
            for person in self.groups[group_number]:
                person.unquarantines()
                # print(f"\t{person.group_number}")
            for person in self.groups[group_number - 1]:
                person.quarantines()
                # print(f"\t{person.group_number}")
        infected_this_round = set()
        recovers_this_round = set()
        for person in self.infected:
            if self.current_time - person.infection_time >= self.recovery_time:
                recovers_this_round.add(person)
            for contact in person.contacts:
                if self.transmission(person, contact):
                    infected_this_round.add(contact)
            if self.symptomatic_quarantine:
                if person.is_symptomatic(self.current_time):
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
            if A.is_contagious(self.current_time) and B.is_susceptible():
                return random.uniform(0, 1) <= self.p
            else:
                return False

    def simulation(self, num_rounds=0):
        if num_rounds:
            for _ in range(num_rounds):
                self.round()
        else:
            while self.infected:
                self.round()


def main():
    return 0


if __name__ == "__main__":
    main()
