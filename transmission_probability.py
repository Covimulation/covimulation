#!/usr/bin/env python3

from sir_graph import SIR_Graph, infection_rate
from contact_distribution import world_pdf

t_p = 0.5
number_of_tests = 10
target_growth_rates = [1 + t / 100 for t in range(5, 31)]
threshold = 0.001
contact_distribution = world_pdf
with open("./output_files/T_p.csv", "w", buffering=1) as tp_file:
    tp_file.write("n,target growth rate,T_p\n")
    for n in [10 ** i for i in range(3, 5)]:
        input_file = f"./input_files/tp_graph_{n}.txt"
        G = SIR_Graph(n=n, p=1, contact_distribution=contact_distribution)
        G.write_to_file(input_file)
        for target_growth_rate in target_growth_rates:
            for i in range(number_of_tests):
                p = infection_rate(
                    target_growth_rate,
                    threshold,
                    contact_distribution,
                    input_file=input_file,
                )
                print(n, i)
                tp_file.write(f"{n},{target_growth_rate},{p}\n")
