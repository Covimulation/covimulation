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
    colors[model_label(mechanisms)] = plt.rcParams["axes.prop_cycle"].by_key()["color"][i]
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


def add_to_plot(plot, X, Y, plot_type, model, label="", alpha=1):
    color = colors[model]
    if plot_type == "growth":
        plot.plot(X, Y, label=label, alpha=alpha, color=color)
    else:
        plot.scatter(X, Y, label=label, alpha=alpha, color=color)


def default_plot(n, p, q, ylabel, t, pdf, model):
    _, plot = plt.subplots(figsize=(16, 9))
    q_string = ""
    if model == "Random Quarantine":
        q_string = f"{100 * q:0.2f}% of population quarantined"
    plot.set_xlabel("Day")
    plot.set_ylabel(ylabel)
    plot.set_title(
        f"""{ylabel} with n = {n}, T_p = {p:0.2f}
            (Average over {t} Simulations)
            Contact Distribution = {pdf}
            {model}
            {q_string}"""
    )
    return plot


def label_func(plot_type):
    if plot_type == "new":
        ylabel = "Number of New Cases"
        data_func = new_cases
    elif plot_type == "growth":
        ylabel = "Growth Rate"
        data_func = growth_rate
    elif plot_type == "total":
        ylabel = "Total Number of Cases"
        data_func = cumulative_total
    return ylabel, data_func


def individual_plots(n, plot_type, x_lim, y_lim):
    ylabel, data_func = label_func(plot_type)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    input_file = os.path.join(
        os.getcwd(), "output_files", "csvs", f"average_growth_data.csv"
    )
    with open(input_file, "r") as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            n = int(row[0])
            pdf = row[1]
            model = row[2]
            p = float(row[3])
            if p == 0:
                continue
            q = float(row[4])
            if model == "Random Quarantine" and q == 0:
                continue
            t = int(row[5])
            X, Y = data_func([float(x) for x in row[6:]])
            plot = default_plot(n, p, q, ylabel, t, pdf, model)
            add_to_plot(plot, X, Y, plot_type, model)
            plot.set_xlim(x_lim[(n, p, q, pdf, model)])
            plot.set_ylim(y_lim[(n, p, q, pdf, model)])
            fig = plot.get_figure()
            file_name = os.path.join(
                os.getcwd(),
                "output_files",
                "plots",
                f"{n}_{plot_type}_{p:0.02f}_{q:0.02f}_{model}_{pdf}.png",
            )
            fig.savefig(file_name)
            plt.close(fig)


def overlaid_plots(n, plot_type, x_lim, y_lim):
    ylabel, data_func = label_func(plot_type)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    input_file = os.path.join(
        os.getcwd(), "output_files", "csvs", f"average_growth_data.csv"
    )
    plots = dict()
    with open(input_file, "r") as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            n = int(row[0])
            pdf = row[1]
            model = row[2]
            p = float(row[3])
            if p == 0:
                continue
            q = float(row[4])
            if model == "Random Quarantine" and q == 0:
                continue
            t = int(row[5])
            X, Y = data_func([float(x) for x in row[6:]])
            key = (n, p, q, pdf)
            if key not in plots:
                plots[key] = default_plot(n, p, q, ylabel, t, pdf, "")
            add_to_plot(plots[key], X, Y, plot_type, model, label=model, alpha=0.7)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    for key, plot in plots.items():
        n, p, q, pdf = key
        x_lim[key] = plot.get_xlim()
        y_lim[key] = plot.get_ylim()
        if plot_type == "total":
            plot.legend(loc="lower right")
        else:
            plot.legend(loc="upper right")
        fig = plot.get_figure()
        file_name = os.path.join(
            os.getcwd(),
            "output_files",
            "plots",
            f"{n}_{plot_type}_{p:0.02f}_{q:0.02f}_{pdf}.png",
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
