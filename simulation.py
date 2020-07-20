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
    # print(f"Took {t:0.3f}s to create graph of {n} nodes.")
    G.write_to_file(output_graph)


def simulation(
    n,
    contact_distribution,
    p,
    T_p,
    mechanism,
    q,
    num_grps,
    schedule,
    asymptomatic_rate,
    initial_infected,
    test_number,
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
        f"growth_data_{n}_{pdf}_{p}_{model}_{T_p}_{q}_{num_grps}_{schedule_string}_{asymptomatic_rate}_{initial_infected}_{test_number}.csv",
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
        asymptomatic_rate=asymptomatic_rate,
        initial_infected=initial_infected,
    )
    G.simulation()
    with open(output_file, "w") as text_file:
        growth_string = ",".join([str(k) for k in G.number_of_new_cases])
        text_file.write(
            f"{G.size},{pdf},{p},{label},{T_p},{q},{num_grps},{schedule_string},{G.asymptomatic_rate},{growth_string}\n"
        )


def schedule(g, t, d):
    arr = []
    for i in range(g):
        for _ in range(t):
            arr.append(i)
    for _ in range(d):
        arr.append(None)
    return arr


def arguments(
    population_pairs,
    pdfs,
    p_values,
    Tp_values,
    mechanisms,
    q_values,
    Schedules,
    asymp_rates,
    num_tests,
):
    args = set()
    for np, pdf, p, T_p, mechanism, q, Schedule, asymp_rate, i in product(
        population_pairs,
        pdfs,
        p_values,
        Tp_values,
        mechanisms,
        q_values,
        Schedules,
        asymp_rates,
        range(num_tests),
    ):
        n, initial_infected = np[0], int(np[0] * np[1])
        if mechanism == "random quarantine":
            arg = (n, pdf, p, T_p, mechanism, q, 1, None, 0, initial_infected, i)
        elif mechanism == "scheduled quarantine":
            k, schedule = Schedule
            arg = (
                n,
                pdf,
                p,
                T_p,
                mechanism,
                None,
                k,
                tuple(schedule),
                asymp_rate,
                initial_infected,
                i,
            )
        elif mechanism == "symptomatic quarantine":
            arg = (
                n,
                pdf,
                p,
                T_p,
                mechanism,
                None,
                1,
                None,
                asymp_rate,
                initial_infected,
                i,
            )
        else:
            arg = (n, pdf, p, T_p, mechanism, None, 1, None, 0, initial_infected, i)
        args.add(arg)
    args = list(args)

    return sorted(args, key=lambda p: (p[0], p[1].__name__, p[2], p[3], p[8]))


def sequential_main():
    number_of_processes = 4
    population_sizes = [10 ** 4, 5 * 10 ** 4]
    asymp_rates = [0.25, 0.3, 0.35, 0.4]
    index_values = [0.001, 0.002, 0.01, 0.02]
    population_pairs = product(population_sizes, index_values)
    number_of_tests = 1
    Tp_values = [0.1]
    # Tp_values = [0.05 * i for i in range(1, 11)]
    p_values = [0, 1]
    q_values = [0.1]
    # q_values = [0.1, 0.2, 0.3, 0.4, 0.5]
    pdfs = [world_pdf]
    schedules = [
        (tup[0], schedule(*tup))
        for tup in [
            (1, 5, 2),
            (1, 4, 3),
            (1, 3, 4),
            (2, 5, 2),
            (2, 3, 3),
            (2, 2, 3),
            (2, 3, 2),
            (3, 3, 0),
            (3, 3, 1),
            (4, 1, 0),
            (5, 1, 0),
            (3, 2, 0),
            (3, 3, 0),
            (2, 4, 0),
        ]
    ]
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    args = arguments(
        population_pairs,
        pdfs,
        p_values,
        Tp_values,
        mechanisms,
        q_values,
        schedules,
        asymp_rates,
        number_of_tests,
    )
    print("Generating graphs.")
    for pdf in pdfs:
        for p in p_values:
            for n in population_sizes:
                create_graph(n, pdf, p)
    print("Finished generating graphs.")
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    finished = 0
    for arg in args:
        print(arg)
        simulation(*arg)
        finished += 1
        print(f"{finished} / {len(args)} ({finished / len(args) * 100 : 0.3f}%) finished")
    csv_helper()
    # plot_helper()


def parallel_main():
    number_of_processes = 4
    population_sizes = [10 ** 4, 5 * 10 ** 4]
    asymp_rates = [0.25, 0.3, 0.35, 0.4]
    index_values = [0.001, 0.002, 0.01, 0.02]
    population_pairs = product(population_sizes, index_values)
    number_of_tests = 1
    Tp_values = [0.1]
    # Tp_values = [0.05 * i for i in range(1, 11)]
    p_values = [0, 1]
    q_values = [0.1]
    # q_values = [0.1, 0.2, 0.3, 0.4, 0.5]
    pdfs = [world_pdf]
    schedules = [
        (tup[0], schedule(*tup))
        for tup in [
            (1, 5, 2),
            (1, 4, 3),
            (1, 3, 4),
            (2, 5, 2),
            (2, 3, 3),
            (2, 2, 3),
            (2, 3, 2),
            (3, 3, 0),
            (3, 3, 1),
            (4, 1, 0),
            (5, 1, 0),
            (3, 2, 0),
            (3, 3, 0),
            (2, 4, 0),
        ]
    ]
    processes = []
    print("Generating graphs.")
    for pdf in pdfs:
        for p in p_values:
            for n in population_sizes:
                process = Process(target=create_graph, args=(n, pdf, p))
                processes.append(process)
                process.start()
    for process in processes:
        process.join()
    print("Finished generating graphs.")
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "csvs", "")):
        os.makedirs(os.path.join(os.getcwd(), "output_files", "csvs", ""))
    args = arguments(
        population_pairs,
        pdfs,
        p_values,
        Tp_values,
        mechanisms,
        q_values,
        schedules,
        asymp_rates,
        number_of_tests,
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
    print(f"Finished {len(args)} simulations. Generating CSVs.")
    csv_helper()
    # print("Finished CSVs. Generating plots.")
    # plot_helper()
    # print("Finished generating plots.")


def main():
    if len(sys.argv) != 1 and sys.argv[1] == "s":
        sequential_main()
    else:
        parallel_main()


if __name__ == "__main__":
    main()
