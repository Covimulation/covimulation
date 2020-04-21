#!/usr/bin/env python3

from sir_graph import SIR_Graph
from contact_distribution import world_pdf
from time import time
from multiprocessing import Process
from collections import defaultdict
from mechanisms import Mechanisms
import csv
import os


def model_string(mechanisms):
    if mechanisms:
        return "_".join(sorted(list(mechanisms))).replace(" ", "_")
    else:
        return "basic_model"


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


def merge_csvs(n, p_values, mechanisms=set(), number_of_tests=1):
    model = model_string(mechanisms)
    output_file = f"./output_files/csvs/growth_data_{n}_{model}.csv"
    with open(output_file, "w") as output_csv:
        output_csv.write(f"n,p,days\n")
        for p in p_values:
            for i in range(number_of_tests):
                input_file = (
                    f"./output_files/csvs/growth_data_{n}_{p:0.02f}_{model}_{i}.csv"
                )
                with open(input_file, "r") as input_csv:
                    for line in input_csv:
                        output_csv.write(line)
                os.remove(input_file)


def add_arrays(A, B):
    if len(A) > len(B):
        return [A[i] + B[i] for i in range(len(B))] + A[len(B) :]
    else:
        return [A[i] + B[i] for i in range(len(A))] + B[len(A) :]


def average_csvs(n, mechanisms):
    model = model_string(mechanisms)
    input_file = f"./output_files/csvs/growth_data_{n}_{model}.csv"
    output_file = f"./output_files/csvs/average_growth_data_{n}_{model}.csv"
    growth_rate = defaultdict(list)
    counts = defaultdict(int)
    with open(input_file, "r") as input_csv:
        reader = csv.reader(input_csv)
        next(reader)
        for row in reader:
            n = int(row[0])
            p = float(row[1])
            data = [int(x) for x in row[2:]]
            growth_rate[p] = add_arrays(growth_rate[p], data)
            counts[p] += 1
    with open(output_file, "w") as output_csv:
        days_string = ",".join([f"day {i}" for i in range(1, 2000)])
        output_csv.write(f"n,p,{days_string}\n")
        for p in growth_rate:
            growth_rate_string = ",".join([str(x / counts[p]) for x in growth_rate[p]])
            output_csv.write(f"{n},{p},{growth_rate_string}\n")


def main():
    contact_distribution = world_pdf
    n = 10 ** 3
    p_values = [0.01 * i for i in range(1, 51)]
    create_graph(n, contact_distribution)
    number_of_processes = 10
    number_of_tests = 1
    for mechanisms in Mechanisms:
        for i in range(10):
            for j in range(number_of_tests):
                processes = []
                for p in p_values[number_of_processes * i : number_of_processes * (i + 1)]:
                    args = (n, p, contact_distribution, set(), j)
                    process = Process(target=simulation, args=args)
                    process.start()
                    processes.append(process)
                for process in processes:
                    process.join()
        merge_csvs(n, p_values, mechanisms, number_of_tests)
    average_csvs(n, mechanisms)


if __name__ == "__main__":
    main()
