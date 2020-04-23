#!/usr/bin/env python3

from sir_graph import SIR_Graph
from contact_distribution import world_pdf
from time import time
from multiprocessing import Process
from mechanisms import Mechanisms, model_string
from csv_helper import csv_helper
import sys


def create_graph(graph_size, contact_distribution):
    output_graph = f"./input_files/tp_graph_{graph_size}.txt"
    t0 = time()
    G = SIR_Graph(n=graph_size, p=1, contact_distribution=contact_distribution)
    t = time() - t0
    print(f"Took {t:0.3f}s to create graph of {graph_size} nodes.")
    G.write_to_file(output_graph)


def simulation(n, p, contact_distribution, mechanisms=set(), test_number=0):
    input_file = f"./input_files/tp_graph_{n}.txt"
    model = model_string(mechanisms)
    output_file = (
        f"./output_files/csvs/growth_data_{n}_{p:0.02f}_{model}_{test_number}.csv"
    )
    G = SIR_Graph(
        p=p,
        contact_distribution=contact_distribution,
        file_name=input_file,
        mechanisms=mechanisms,
    )
    G.simulation()
    with open(output_file, "w") as text_file:
        growth_string = ",".join([str(k) for k in G.number_of_new_cases])
        text_file.write(f"{G.size},{p},{growth_string}\n")


def main():
    contact_distribution = world_pdf
    if len(sys.argv) == 1:
        n = 10 ** 6
    else:
        n = int(sys.argv[1])
    p_values = [0.01, 0.02, 0.03, 0.04, 0.05]
    # p_values = [0.01 * i for i in range(1, 51)]
    create_graph(n, contact_distribution)
    number_of_processes = 10
    number_of_tests = 10
    args = [
        (n, p, contact_distribution, mechanisms, j)
        for p in p_values
        for mechanisms in Mechanisms
        for j in range(number_of_tests)
    ]
    for i in range(len(args) // number_of_processes):
        processes = []
        for arg in args[i * number_of_processes : (i + 1) * number_of_processes]:
            process = Process(target=simulation, args=arg)
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
    for mechanisms in Mechanisms:
        csv_helper(n, p_values, mechanisms, number_of_tests)


if __name__ == "__main__":
    main()
