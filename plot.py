#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv
from mechanisms import Mechanisms, model_string


def plot_average_growth_rate(n, p, number_of_new_cases, mechanisms):
    number_of_days = len(number_of_new_cases)
    model = model_string(mechanisms)
    fig = plt.figure()
    plot = fig.add_subplot(1, 1, 1)
    plot.set_xlabel("Day")
    plot.set_ylabel("Number of New Cases")
    plot.set_title(
        f"Number of New Cases with n = {n}, T_p = {p:0.2f}\n(Average over 10 Simulations)\nModel = {model}"
    )

    X = np.array(range(1, number_of_days + 1))
    Y = np.array(number_of_new_cases)
    plt.scatter(X, Y)
    plt.savefig(f"./output_files/plots/average_plot_{n}_{p:0.2f}_{model}.png")


def main():
    for mechanisms in Mechanisms:
        model = model_string(mechanisms)
        input_file = f"./output_files/csvs/average_growth_data_1000_{model}.csv"
        with open(input_file, "r") as data_file:
            rows = csv.reader(data_file)
            next(rows)
            for row in rows:
                n, p = int(row[0]), float(row[1])
                data = [float(x) for x in row[2:]]
                plot_average_growth_rate(n, p, data, mechanisms)


if __name__ == "__main__":
    main()
