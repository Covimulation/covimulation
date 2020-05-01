#!/usr/bin/env python3

import matplotlib.pyplot as plt
import csv
from mechanisms import Mechanisms, model_string, model_label
import os
import sys
from collections import defaultdict

colors = dict()
i = 0
for mechanisms in Mechanisms:
    colors[mechanisms] = plt.rcParams["axes.prop_cycle"].by_key()["color"][i]
    i += 1


def growth_rate(data):
    X, Y = [], []
    for i in range(1, len(data)):
        prev, curr = data[i - 1], data[i]
        if prev != 0:
            X.append(i)
            Y.append(curr / prev)
    return X, Y


def cumulative_total(data):
    X = list(range(1, len(data) + 1))
    Y = [sum(data[:i]) for i in range(1, len(data) + 1)]
    return X, Y


def new_cases(data):
    X, Y = [], []
    for i, num in enumerate(data):
        if data[i] != 0:
            X.append(i + 1)
            Y.append(num)
    return X, Y


def add_to_plot(plot, X, Y, plot_type, mechanisms, label="", alpha=1):
    color = colors[mechanisms]
    if plot_type == "growth":
        plot.plot(X, Y, label=label, alpha=alpha, color=color)
    else:
        plot.scatter(X, Y, label=label, alpha=alpha, color=color)


def default_plot(n, p, ylabel, mechanisms=None):
    _, plot = plt.subplots(figsize=(16, 9))
    plot.set_xlabel("Day")
    plot.set_ylabel(ylabel)
    if mechanisms is None:
        plot.set_title(
            f"{ylabel} with n = {n}, T_p = {p:0.2f}\n(Average over 10 Simulations)"
        )
    else:
        title = model_label(mechanisms)
        plot.set_title(
            f"{ylabel} with n = {n}, T_p = {p:0.2f}\n(Average over 10 Simulations)\n{title}"
        )
    return plot


def label_func(plot_type):
    if plot_type == "new":
        ylabel = "Number of New Cases"
        func = new_cases
    elif plot_type == "growth":
        ylabel = "Growth Rate"
        func = growth_rate
    elif plot_type == "total":
        ylabel = "Total Number of Cases"
        func = cumulative_total
    return ylabel, func


def individual_plots(n, plot_type, x_lim, y_lim):
    ylabel, func = label_func(plot_type)
    plots = dict()
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    for mechanisms in Mechanisms:
        model = model_string(mechanisms)
        input_file = os.path.join(
            os.getcwd(), "output_files", "csvs", f"average_growth_data_{n}_{model}.csv"
        )
        with open(input_file, "r") as file:
            rows = csv.reader(file)
            next(rows)
            for row in rows:
                n = int(row[0])
                p = float(row[1])
                X, Y = func([float(x) for x in row[2:]])
                if (p, mechanisms) not in plots:
                    plots[(p, mechanisms)] = default_plot(n, p, ylabel, mechanisms)
                add_to_plot(
                    plots[(p, mechanisms)], X, Y, plot_type, mechanisms, label="", alpha=1
                )
    for (p, mechanisms), plot in plots.items():
        plot.set_xlim(x_lim[p])
        plot.set_ylim(y_lim[p])
        fig = plot.get_figure()
        file_name = os.path.join(
            os.getcwd(),
            "output_files",
            "plots",
            f"{plot_type}_{p}_{model_string(mechanisms)}.png",
        )
        fig.savefig(file_name)
        plt.close(fig)


def overlaid_plots(n, plot_type, x_lim, y_lim):
    ylabel, func = label_func(plot_type)
    plots = dict()
    for mechanisms in Mechanisms:
        model = model_string(mechanisms)
        input_file = os.path.join(
            os.getcwd(), "output_files", "csvs", f"average_growth_data_{n}_{model}.csv"
        )
        with open(input_file, "r") as file:
            rows = csv.reader(file)
            next(rows)
            for row in rows:
                n = int(row[0])
                p = float(row[1])
                X, Y = func([float(x) for x in row[2:]])
                label = model_label(mechanisms)
                if p not in plots:
                    plots[p] = default_plot(n, p, ylabel)
                add_to_plot(plots[p], X, Y, plot_type, mechanisms, label=label, alpha=1)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    for p, plot in plots.items():
        x_lim[p] = plot.get_xlim()
        y_lim[p] = plot.get_ylim()
        if plot_type == "total":
            plot.legend(loc="lower right")
        else:
            plot.legend(loc="upper right")
        fig = plot.get_figure()
        file_name = os.path.join(
            os.getcwd(), "output_files", "plots", f"{plot_type}_{p}.png"
        )
        fig.savefig(file_name)
        plt.close(fig)


def main():
    if len(sys.argv) == 1:
        print("Invalid commandline arguments.")
        n = int(input("Please input the number of nodes.\n"))
    else:
        n = int(sys.argv[1])
    plot_types = ["new", "growth", "total"]
    x_lim, y_lim = defaultdict(int), defaultdict(int)
    for plot_type in plot_types:
        overlaid_plots(n, plot_type, x_lim, y_lim)
        individual_plots(n, plot_type, x_lim, y_lim)


if __name__ == "__main__":
    main()
