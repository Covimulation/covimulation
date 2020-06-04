#!/usr/bin/env python3

from sir_graph import SIR_Graph
from contact_distribution import world_pdf
from time import time
from multiprocessing import Process
from mechanisms import mechanisms, model_string, model_label
from csv_helper import csv_helper
import os
import shutil
import sys
from itertools import product


def create_graph(n, contact_distribution):
    cwd = os.getcwd()
    pdf = contact_distribution.__name__
    if not os.path.isdir(os.path.join(cwd, "input_files", "")):
        os.mkdir(os.path.join(cwd, "input_files", ""))
    output_graph = os.path.join(cwd, "input_files", f"tp_graph_{n}_{pdf}.txt")
    t0 = time()
    G = SIR_Graph(n=n, p=1, contact_distribution=contact_distribution)
    t = time() - t0
    print(f"Took {t:0.3f}s to create graph of {n} nodes.")
    G.write_to_file(output_graph)


def simulation(
    n, contact_distribution, p, T_p, mechanism, q, num_grps, schedule, test_number
):
    cwd = os.getcwd()
    pdf = contact_distribution.__name__
    input_file = os.path.join(cwd, "input_files", f"tp_graph_{n}_{pdf}.txt")
    model = model_string(mechanism)
    label = model_label(mechanism)
    output_file = os.path.join(
        cwd,
        "output_files",
        "csvs",
        f"growth_data_{n}_{T_p}_{q}_{model}_{num_grps}_{test_number}_{pdf}.csv",
    )
    G = SIR_Graph(
        p=p,
        contact_distribution=contact_distribution,
        file_name=input_file,
        mechanism=mechanism,
        quarantine_probability=q,
        number_of_groups=num_grps,
    )
    G.simulation()
    with open(output_file, "w") as text_file:
        growth_string = ",".join([str(k) for k in G.number_of_new_cases])
        text_file.write(f"{G.size},{pdf},{label},{T_p},{q},{num_grps},{growth_string}\n")


def schedule(g, t, d):
    arr = []
    for i in range(g):
        for _ in range(t):
            arr.append(i)
    for _ in range(d):
        arr.append(None)
    return arr


def arguments(n, pdfs, Tp_values, mechanisms, q_values, group_sizes, num_tests):
    args = set()
    for pdf, T_p, mechanism, q, k, i in product(
        pdfs, Tp_values, mechanisms, q_values, group_sizes, range(num_tests)
    ):
        if mechanism == "random quarantine":
            arg = (n, pdf, T_p, mechanism, q, None, i)
        elif mechanism == "scheduled quarantine":
            arg = (n, pdf, T_p, mechanism, None, k, i)
        else:
            arg = (n, pdf, T_p, mechanism, None, None, i)
        args.add(arg)
    args = list(args)

    return sorted(args, key=lambda p: (p[0], p[1].__name__, p[2], p[6]))


def sequential_main():
    n = 10 ** 6
    number_of_tests = 10
    # p_values = [0.025 * i for i in range(1, 41)]
    Tp_values = [0.01, 0.1, 0.2, 0.5]
    q_values = [0.1 * i for i in range(1, 10)]
    group_sizes = range(2, 8)
    pdfs = [world_pdf]
    for pdf in pdfs:
        create_graph(n, pdf)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    args = arguments(
        n, pdfs, Tp_values, mechanisms, q_values, group_sizes, number_of_tests
    )
    for arg in args:
        simulation(*arg)
    csv_helper()


def parallel_main():
    # n = int(input("Please input the number of nodes.\n"))
    # number_of_tests = int(input("Please input the number of tests.\n"))
    # p_values = [
    #     float(p) for p in input("Please input space-separated p-values\n").split(" ")
    # ]
    # q_values = [
    #     float(q) for q in input("Please input space-separated q-values\n").split(" ")
    # ]
    n = 5 * 10 ** 4
    number_of_tests = 10
    # p_values = [0.025 * i for i in range(1, 41)]
    Tp_values = [0.025 * i for i in range(21)]
    q_values = [0.1 * i for i in range(1, 10)]
    group_sizes = range(2, 8)
    pdfs = [world_pdf]
    num_tests = 10
    for pdf in pdfs:
        create_graph(n, pdf)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    number_of_processes = 100
    args = arguments(n, pdfs, Tp_values, mechanisms, q_values, group_sizes, num_tests,)
    for i in range(len(args) // number_of_processes + 1):
        processes = []
        for arg in args[i * number_of_processes : (i + 1) * number_of_processes]:
            process = Process(target=simulation, args=arg)
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
    csv_helper()


def main():
    if len(sys.argv) != 1:
        if sys.argv[1] == "s":
            sequential_main()
    else:
        parallel_main()


if __name__ == "__main__":
    main()
