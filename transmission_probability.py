#!/usr/bin/env python3

from sir_graph import SIR_Graph, infection_rate
from contact_distribution import world_pdf
from time import time
from multiprocessing import Process, Condition


def create_graph(graph_size, contact_distribution):
    input_file = f"./input_files/tp_graph_{graph_size}.txt"
    t0 = time()
    G = SIR_Graph(n=graph_size, p=1, contact_distribution=contact_distribution)
    t = time() - t0
    print(f"Took {t:0.3f}s to create graph of {graph_size} nodes.")
    G.write_to_file(input_file)
    return


def tp_simulation(n, target_growth_rate, threshold, contact_distribution, test_number):
    input_file = f"./input_files/tp_graph_{n}.txt"
    # t0 = time()
    p = infection_rate(
        target_growth_rate,
        threshold,
        contact_distribution,
        input_file=input_file,
        output_file=f"./output_files/growth_data_{n}_{target_growth_rate}_{test_number}.csv",
    )
    # t = time() - t0
    # print(
    #     f"Took {t:0.3f}s to determine T_p of {p:0.3f} for target growth rate of {target_growth_rate:0.2f} on {n} nodes."
    # )


# def sequential_main(number_of_tests=3, threshold=0.001):
#     target_growth_rates = [1 + t / 100 for t in range(5, 31)]
#     contact_distribution = world_pdf
#     graph_sizes = [10 ** i for i in range(3, 5)]
#     for graph_size in graph_sizes:
#         create_graph(graph_size, contact_distribution)
#         for target_growth_rate in target_growth_rates:
#             for test_number in range(number_of_tests):
#                 tp_simulation(
#                     graph_size,
#                     target_growth_rate,
#                     threshold,
#                     contact_distribution,
#                     test_number,
#                 )


# def main(number_of_tests=3, threshold=0.001):
#     # target_growth_rates = [1 + t / 100 for t in range(5, 31)]
#     contact_distribution = world_pdf
#     graph_sizes = [10 ** i for i in range(3, 5)]
#     for graph_size in graph_sizes:
#         p = Process(target=create_graph, args=(graph_size, contact_distribution))
#         p.start()
#         p.join()
#     for graph_size in graph_sizes:
#         for target_growth_rate in [1.1]:
#             for test_number in range(number_of_tests):
#                 q = Process(
#                     target=tp_simulation,
#                     args=(
#                         graph_size,
#                         target_growth_rate,
#                         threshold,
#                         contact_distribution,
#                         test_number,
#                     ),
#                 )
#                 q.start()


def main():
    target_growth_rate = 1.1
    contact_distribution = world_pdf
    n = 10 ** 6
    create_graph(n, contact_distribution)
    for test_number in range(5):
        q = Process(
            target=tp_simulation,
            args=(n, target_growth_rate, 0.001, contact_distribution, test_number),
        )
        q.start()


# def main():
#     target_growth_rate = 1.1
#     contact_distribution = world_pdf
#     n = 10 ** 6
#     create_graph(n, contact_distribution)
#     for test_number in range(2):
#         tp_simulation(n, target_growth_rate, 0.001, contact_distribution, test_number)


if __name__ == "__main__":
    main()
