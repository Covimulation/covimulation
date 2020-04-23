#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv
from mechanisms import Mechanisms, model_string, model_label
import os


def growth_rate(data):
    inf = float("inf")
    growth_array = [inf]
    for i in range(1, len(data)):
        prev, curr = data[i - 1], data[i]
        if prev == 0:
            growth_array.append(inf)
        else:
            growth_array.append(curr / prev)
    return growth_array


def cumulative_total(data):
    return [sum(data[:i]) for i in range(1, len(data) + 1)]


def identity(x):
    return x


def add_to_plot(plot, array, label):
    number_of_days = len(array)
    X = np.array(range(1, number_of_days + 1))
    Y = array
    plot.plot(X, Y, label=label, alpha=0.7)


def default_plot(n, p, ylabel):
    _, plot = plt.subplots(figsize=(16, 9))
    plot.set_xlabel("Day")
    plot.set_ylabel(ylabel)
    plot.set_title(
        f"{ylabel} with n = {n}, T_p = {p:0.2f}\n(Average over 10 Simulations)\n"
    )
    return plot


def plots(n, plot_type):
    if plot_type == "new":
        ylabel = "Number of New Cases"
        func = identity
    elif plot_type == "growth":
        ylabel = "Growth Rate"
        func = growth_rate
    elif plot_type == "total":
        ylabel = "Total Number of Cases"
        func = cumulative_total
    else:
        return

    plots = dict()
    for mechanisms in Mechanisms:
        model = model_string(mechanisms)
        input_file = f"./output_files/csvs/average_growth_data_{n}_{model}.csv"
        with open(input_file, "r") as file:
            rows = csv.reader(file)
            next(rows)
            for row in rows:
                n = int(row[0])
                p = float(row[1])
                data = func([float(x) for x in row[2:]])
                label = model_label(mechanisms)
                if p not in plots:
                    plots[p] = default_plot(n, p, ylabel)
                add_to_plot(plots[p], data, label)
    if not os.path.isdir("./output_files/plots"):
        os.mkdir("./output_files/plots")
    for p, plot in plots.items():
        plot.legend(loc="upper right")
        fig = plot.get_figure()
        fig.savefig(f"./output_files/plots/{plot_type}_{p}.png")


def main(n=1000000):
    plot_types = ["new", "growth", "total"]
    for plot_type in plot_types:
        plots(n, plot_type)


if __name__ == "__main__":
    main()
