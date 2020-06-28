#!/usr/bin/env python3

from sir_graph import SIR_Graph
from contact_graph import Contact_Graph
from contact_distribution import world_pdf
from time import time
from multiprocessing import Process
from mechanisms import mechanisms, model_string, model_label
from csv_helper import csv_helper
import os
import shutil
import sys
from itertools import product
from plot_helper import plot_helper


def create_graph(n, contact_distribution, p):
    cwd = os.getcwd()
    pdf = contact_distribution.__name__
    if not os.path.isdir(os.path.join(cwd, "input_files", "")):
        os.mkdir(os.path.join(cwd, "input_files", ""))
    output_graph = os.path.join(cwd, "input_files", f"tp_graph_{n}_{pdf}_{p}.txt")
    t0 = time()
    G = Contact_Graph(contact_distribution, n, p=p)
    t = time() - t0
    print(f"Took {t:0.3f}s to create graph of {n} nodes.")
    G.write_to_file(output_graph)


def simulation(
    n, contact_distribution, p, T_p, mechanism, q, num_grps, schedule, test_number
):
    cwd = os.getcwd()
    pdf = contact_distribution.__name__
    input_file = os.path.join(cwd, "input_files", f"tp_graph_{n}_{pdf}_{p}.txt")
    model = model_string(mechanism)
    label = model_label(mechanism)
    if schedule:
        schedule_string = " ".join([str(x) for x in schedule])
    else:
        schedule_string = "None"
    output_file = os.path.join(
        cwd,
        "output_files",
        "csvs",
        f"growth_data_{n}_{pdf}_{p}_{model}_{T_p}_{q}_{num_grps}_{schedule_string}_{test_number}.csv",
    )
    G = SIR_Graph(
        T_p=T_p,
        contact_distribution=contact_distribution,
        file_name=input_file,
        mechanism=mechanism,
        quarantine_probability=q,
        number_of_groups=num_grps,
        schedule=schedule,
        p=p,
    )
    G.simulation()
    with open(output_file, "w") as text_file:
        growth_string = ",".join([str(k) for k in G.number_of_new_cases])
        text_file.write(
            f"{G.size},{pdf},{p},{label},{T_p},{q},{num_grps},{schedule_string},{growth_string}\n"
        )


def schedule(g, t, d):
    arr = []
    for i in range(g):
        for _ in range(t):
            arr.append(i)
    for _ in range(d):
        arr.append(None)
    return arr


def arguments(n, pdfs, p_values, Tp_values, mechanisms, q_values, Schedules, num_tests):
    args = set()
    for pdf, p, T_p, mechanism, q, Schedule, i in product(
        pdfs, p_values, Tp_values, mechanisms, q_values, Schedules, range(num_tests),
    ):
        if mechanism == "random quarantine":
            arg = (n, pdf, p, T_p, mechanism, q, 1, None, i)
        elif mechanism == "scheduled quarantine":
            k, schedule = Schedule
            arg = (n, pdf, p, T_p, mechanism, None, k, tuple(schedule), i)
        else:
            arg = (n, pdf, p, T_p, mechanism, None, 1, None, i)
        args.add(arg)
    args = list(args)

    return sorted(args, key=lambda p: (p[0], p[1].__name__, p[2], p[3], p[8]))


def sequential_main():
    n = 5 * 10 ** 4
    number_of_tests = 10
    # p_values = [0.025 * i for i in range(1, 41)]
    Tp_values = [0.1, 0.2, 0.3, 0.4, 0.5]
    # p_values = [0.8, 0.85, 0.9, 0.95, 1]
    p_values = [1]
    q_values = [0.1]
    pdfs = [world_pdf]
    # schedules = [
    #     (tup[0], schedule(*tup))
    #     for tup in [
    #         (1, 5, 2),
    #         (1, 4, 3),
    #         (1, 3, 4),
    #         (2, 5, 2),
    #         (2, 3, 3),
    #         (2, 2, 3),
    #         (2, 3, 2),
    #         (3, 3, 0),
    #         (3, 3, 1),
    #         (4, 1, 0),
    #     ]
    # ]
    schedules = [(tup[0], schedule(*tup)) for tup in [(1, 5, 2)]]
    for pdf in pdfs:
        for p in p_values:
            create_graph(n, pdf, p)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    args = arguments(
        n, pdfs, p_values, Tp_values, mechanisms, q_values, schedules, number_of_tests,
    )
    finished = 0
    for arg in args:
        simulation(*arg)
        finished += 1
        print(f"{finished} / {len(args)} ({finished / len(args) * 100 : 0.3f}%) finished")
    csv_helper()
    plot_helper()


def parallel_main():
    number_of_processes = 8
    n = 5 * 10 ** 4
    number_of_tests = 10
    # p_values = [0.025 * i for i in range(1, 41)]
    Tp_values = [0.1, 0.2, 0.3, 0.4, 0.5]
    # p_values = [0.8, 0.85, 0.9, 0.95, 1]
    p_values = [1]
    q_values = [0.1]
    pdfs = [world_pdf]
    # schedules = [
    #     (tup[0], schedule(*tup))
    #     for tup in [
    #         (1, 5, 2),
    #         (1, 4, 3),
    #         (1, 3, 4),
    #         (2, 5, 2),
    #         (2, 3, 3),
    #         (2, 2, 3),
    #         (2, 3, 2),
    #         (3, 3, 0),
    #         (3, 3, 1),
    #         (4, 1, 0),
    #     ]
    # ]
    schedules = [(tup[0], schedule(*tup)) for tup in [(1, 5, 2)]]
    for pdf in pdfs:
        for p in p_values:
            create_graph(n, pdf, p)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    args = arguments(
        n, pdfs, p_values, Tp_values, mechanisms, q_values, schedules, number_of_tests,
    )
    finished = 0
    for i in range(len(args) // number_of_processes + 1):
        print(f"{finished} / {len(args)} ({finished / len(args) * 100 : 0.3f}%) finished")
        processes = []
        for arg in args[i * number_of_processes : (i + 1) * number_of_processes]:
            process = Process(target=simulation, args=arg)
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
        finished += number_of_processes
    csv_helper()
    plot_helper()


def main():
    if len(sys.argv) != 1 and sys.argv[1] == "s":
        sequential_main()
    else:
        parallel_main()


if __name__ == "__main__":
    main()
