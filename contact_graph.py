#!/usr/bin/env python3

import random
import math
from grid import Grid
from person import Person
from contact_distribution import world_pdf


class Contact_Graph:
    def __init__(self, contact_distribution, n=0, file_name=None, t=None, a=0, b=1):
        if file_name:
            self.read_from_file(file_name)
        else:
            self.size = n
            self.contact_distribution = contact_distribution
            self.a = a
            self.b = b
            self.people = set()
            if t is None:
                print(n)
                self.t = int(math.sqrt(n / math.log(n)))
            else:
                self.t = t
            self.Grid = Grid(self.t, a)
            for i in range(n):
                self.create_person(i)
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
        v = Person(id, coordinates, self.contact_distribution)
        self.add_person(v)

    def update_contacts(self, u):
        i = 0
        while len(u.contacts) < u.number_of_contacts + 1 and i < self.t - min(u.sector):
            s = len(u.contacts)
            new_nodes = self.Grid.adjacent_nodes(u, i)
            if s + len(new_nodes) > u.number_of_contacts + 1:
                new_nodes = sorted(list(new_nodes), key=lambda v: u.distance(v))
                new_nodes = set(new_nodes[: u.number_of_contacts - s])
            u.contacts = u.contacts.union(self.Grid.adjacent_nodes(u, i))
            i += 1
        if u in u.contacts:
            u.contacts.remove(u)

    def write_to_file(self, file_name):
        with open(file_name, "w") as text_file:
            text_file.write(f"{self.size} {self.a} {self.b}\n")
            for person in self.people:
                text_file.write(f"{person.id} ")
                contacts = [str(contact.id) for contact in person.contacts]
                text_file.write(f"{' '.join(contacts)} ")
                coordinates = [str(x) for x in person.coordinates]
                text_file.write(f"{' '.join(coordinates)}\n")

    def read_from_file(self, file_name):
        with open(file_name, "r") as text_file:
            line = text_file.readline().split(" ")
            self.size = int(line[0])
            self.a = float(line[1])
            self.b = float(line[2])
            people_array = [Person(id, (0, 0), None) for id in range(self.size)]
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
