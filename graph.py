#!/usr/bin/env python3

from vertex import Vertex


class Graph:
    def __init__(self, vertices, directed=False):
        if isinstance(vertices, str):
            self.read_from_text_file(vertices)
        else:
            self.vertices = vertices
            self.directed = directed
            self.size = len(vertices)

    def add_vertex(self, u):
        for v in self.vertices:
            if u.has_neighbor(v):
                v.add_neighbor(u)
        self.vertices.add(u)
        self.size += 1

    def print_graph(self, increasing=True):
        if increasing:
            for vertex in sorted(self.vertices, key=lambda v: v.id):
                print(vertex.id)
                print("\t", end="")
                vertex.print_neighbors()
        else:
            for vertex in self.vertices:
                print(vertex.id)
                print("\t", end="")
                vertex.print_neighbors()

    def write_to_file(self, file_name):
        with open(file_name, "w") as text_file:
            text_file.write(f"{self.size} {self.directed}\n")
            for vertex in self.vertices:
                text_file.write(
                    f"{vertex.id} {' '.join([str(neighbor.id) for neighbor in vertex.neighbors])}\n"
                )
        return

    def read_from_file(self, file_name):
        with open(file_name, "r") as text_file:
            line = text_file.readline().split(" ")
            self.size = int(line[0])
            self.directed = bool(line[1])
            vertices_array = [Vertex(i, set()) for i in range(self.size)]
            for line in text_file:
                data = [int(id) for id in line.split(" ")]
                id = data[0]
                neighbor_ids = data[1:]
                u = vertices_array[id]
                for neighbor_id in neighbor_ids:
                    v = vertices_array[neighbor_id]
                    u.add_neighbor(v)
            self.vertices = set(vertices_array)
        return


def main():
    vertices = set()
    for i in range(10):
        vertices.add(Vertex(i, []))
    for u in vertices:
        for v in vertices:
            if u.id != v.id:
                u.add_neighbor(v)
    G = Graph(vertices)
    G.write_to_file("test.txt")
    H = Graph("test.txt")
    H.write_to_file("test2.txt")


if __name__ == "__main__":
    main()
