#!/usr/bin/env python3

import random
import math
from grid import Grid
from person import Person
from contact_distribution import world_pdf
from alias_sampler import vose_alias_method_sampler, sample_without_replacement


class Contact_Graph:
    __slots__ = [
        "size",
        "contact_distribution",
        "a",
        "b",
        "p",
        "people",
        "weights",
        "t",
        "Grid",
        "degree_distribution",
        "number_of_groups",
    ]

    def __init__(
        self,
        contact_distribution,
        n=0,
        *,
        file_name=None,
        t=None,
        a=0,
        b=1,
        number_of_groups=1,
        p=1,
    ):
        self.number_of_groups = number_of_groups
        if file_name:
            self.read_from_file(file_name)
        else:
            self.size = n
            self.contact_distribution = contact_distribution
            self.a = a
            self.b = b
            self.p = p
            self.people = set()
            self.weights = dict()
            if t is None:
                self.t = int(math.sqrt(n / math.log(n)))
            else:
                self.t = t
            self.Grid = Grid(self.t, a)
            for i in range(n):
                self.create_person(i)
            self.degree_distribution = vose_alias_method_sampler(
                self.weights.values(), self.weights.keys()
            )
            for u in self.people:
                self.update_contacts(u)
            for u in self.people:
                for v in u.contacts:
                    v.contacts.add(u)

    def add_person(self, u):
        self.people.add(u)
        self.Grid.assign_sector(u)

    def create_person(self, id):
        coordinates = []
        for _ in range(2):
            coordinates.append(random.uniform(self.a, self.b))
        v = Person(id, coordinates, self.contact_distribution, self.number_of_groups)
        self.weights[v] = v.number_of_contacts
        self.add_person(v)

    def update_contacts(self, u):
        number_of_close_neighbors = sum(
            random.uniform(0, 1) <= self.p for _ in range(u.number_of_contacts)
        )
        number_of_random_neighbors = u.number_of_contacts - number_of_close_neighbors
        i, s = 0, 0
        nearest_neighbors = []
        k = number_of_close_neighbors + 1
        while s < k:
            s = len(nearest_neighbors)
            new_nodes = self.Grid.adjacent_nodes(u, i)
            if s + len(new_nodes) > k:
                new_nodes = sorted(list(new_nodes), key=lambda v: u.distance(v))
                new_nodes = new_nodes[: k - s]
            nearest_neighbors += sorted(new_nodes, key=lambda v: u.distance(v))
            i += 1
        del nearest_neighbors[0]
        nearest_neighbors = set(nearest_neighbors[:number_of_close_neighbors])
        random_neighbors = set(
            sample_without_replacement(
                number_of_random_neighbors,
                self.degree_distribution,
                skip=nearest_neighbors,
            )
        )
        u.contacts = u.contacts.union(nearest_neighbors).union(random_neighbors)
        if len(u.contacts) != u.number_of_contacts:
            print(u.id, u.number_of_contacts, len([v.id for v in u.contacts]))

    def write_to_file(self, file_name):
        with open(file_name, "w") as text_file:
            text_file.write(f"{self.size} {self.a} {self.b}\n")
            for person in self.people:
                text_file.write(f"{person.id} ")
                contacts = [str(contact.id) for contact in person.contacts]
                if contacts:
                    text_file.write(f"{' '.join(contacts)} ")
                coordinates = [str(x) for x in person.coordinates]
                text_file.write(f"{' '.join(coordinates)}\n")

    def read_from_file(self, file_name):
        with open(file_name, "r") as text_file:
            line = text_file.readline().split(" ")
            self.size = int(line[0])
            self.a = float(line[1])
            self.b = float(line[2])
            people_array = [
                Person(id, (0, 0), None, self.number_of_groups) for id in range(self.size)
            ]
            for line in text_file:
                data = line.split(" ")
                id = int(data[0])
                contact_ids = [int(x) for x in data[1:-2]]
                person = people_array[id]
                for contact_id in contact_ids:
                    contact = people_array[contact_id]
                    person.add_contact(contact)
                    person.number_of_contacts += 1
        self.people = set(people_array)

    def print_graph(self):
        for person in sorted(list(self.people), key=lambda person: person.id):
            contacts = sorted(list(person.contacts), key=lambda contact: contact.id)
            print(f"{person.id}: {[contact.id for contact in contacts]}")


def main():
    random.seed(1)
    G = Contact_Graph(n=10 ** 2, contact_distribution=world_pdf)
    G.write_to_file("test.txt")
    H = Contact_Graph(file_name="test.txt", contact_distribution=world_pdf)
    H.print_graph()
    # for v in sorted(list(G.vertices), key=lambda v: v.id):
    #     print(v.id)
    #     print(v.coordinates)
    #     v.print_neighbors(increasing=True)


if __name__ == "__main__":
    main()
