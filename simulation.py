#!/usr/bin/env python3

from sir_graph import SIR_Graph
from contact_distribution import world_pdf
from time import time
from multiprocessing import Process
from mechanisms import Mechanisms, model_string, model_label
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


def simulation(n, p, contact_distribution, mechanisms=set(), test_number=0, q=0):
    cwd = os.getcwd()
    pdf = contact_distribution.__name__
    input_file = os.path.join(cwd, "input_files", f"tp_graph_{n}_{pdf}.txt")
    model = model_string(mechanisms)
    label = model_label(mechanisms)
    output_file = os.path.join(
        cwd,
        "output_files",
        "csvs",
        f"growth_data_{n}_{p:0.02f}_{q:0.02f}_{model}_{test_number}_{pdf}.csv",
    )
    G = SIR_Graph(
        p=p,
        contact_distribution=contact_distribution,
        file_name=input_file,
        mechanisms=mechanisms,
        quarantine_probability=q,
    )
    G.simulation()
    with open(output_file, "w") as text_file:
        growth_string = ",".join([str(k) for k in G.number_of_new_cases])
        text_file.write(f"{G.size},{pdf},{label},{p},{q},{growth_string}\n")


def arguments(n, p_values, pdfs, Mechanisms, num_tests, q_values):
    args = []
    for p, mechanisms in product(p_values, Mechanisms):
        if p in {0, 1}:
            k = 1
        else:
            k = num_tests
        if "random quarantine" in mechanisms:
            args += [
                (n, p, pdf, mechanisms, i, q)
                for i in range(k)
                for pdf in pdfs
                for q in q_values
            ]
        else:
            args += [(n, p, pdf, mechanisms, i, 0) for i in range(k) for pdf in pdfs]
    return args


def main():
    # n = int(input("Please input the number of nodes.\n"))
    # number_of_tests = int(input("Please input the number of tests.\n"))
    # p_values = [
    #     float(p) for p in input("Please input space-separated p-values\n").split(" ")
    # ]
    # q_values = [
    #     float(q) for q in input("Please input space-separated q-values\n").split(" ")
    # ]
    n = 10 ** 6
    number_of_tests = 10
    # p_values = [0.025 * i for i in range(1, 41)]
    # q_values = [0.1 * i for i in range(1, 10)]
    p_values = [0.025]
    q_values = [0.1]
    pdfs = [world_pdf]
    for pdf in pdfs:
        create_graph(n, pdf)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    number_of_processes = 10
    args = arguments(n, p_values, pdfs, Mechanisms, number_of_tests, q_values)
    for i in range(len(args) // number_of_processes + 1):
        processes = []
        for arg in args[i * number_of_processes : (i + 1) * number_of_processes]:
            process = Process(target=simulation, args=arg)
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
    for p in {0, 1}:
        if p in p_values:
            for mechanisms in Mechanisms:
                model = model_string(mechanisms)
                for pdf in pdfs:
                    if "random quarantine" not in mechanisms:
                        my_q_values = [0]
                    else:
                        my_q_values = q_values
                    for q in my_q_values:
                        input_file = os.path.join(
                            os.getcwd(),
                            "output_files",
                            "csvs",
                            f"growth_data_{n}_{p:0.02f}_{q:0.02f}_{model}_0_{pdf.__name__}.csv",
                        )
                        for i in range(1, number_of_tests):
                            output_file = os.path.join(
                                os.getcwd(),
                                "output_files",
                                "csvs",
                                f"growth_data_{n}_{p:0.02f}_{q:0.02f}_{model}_{i}_{pdf.__name__}.csv",
                            )
                            shutil.copyfile(input_file, output_file)

    csv_helper()


if __name__ == "__main__":
    main()
