#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import csv
from mechanisms import mechanisms, model_string, model_label
import os
import sys
from collections import defaultdict
from itertools import product

colors = dict()
i = 0
for mechanism in mechanisms:
    colors[model_label(mechanism)] = plt.rcParams["axes.prop_cycle"].by_key()["color"][i]
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


def add_to_plot(plot, X, Y, plot_type, model, legend_label="", alpha=1):
    color = colors[model]
    if plot_type == "growth":
        plot.plot(X, Y, label=legend_label, alpha=alpha, color=color)
    else:
        plot.scatter(X, Y, label=legend_label, alpha=alpha, color=color)


def default_plot(n, p, ylabel, t, model=None, string=None):
    _, plot = plt.subplots(figsize=(16, 9))
    plot.set_xlabel("Day")
    plot.set_ylabel(ylabel)
    title = f"{ylabel} with n = {n}, T_p = {p:0.2f}\n(Average over {t} Simulations)"
    if model:
        title = f"{title}\n{model}"
    if string:
        title = f"{title}\n{string}"
    plot.set_title(title)
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


def individual_plots(plot_type, x_lim, y_lim):
    ylabel, func = label_func(plot_type)
    plots = dict()
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    input_file = os.path.join(
        os.getcwd(), "output_files", "csvs", "average_growth_data.csv"
    )
    with open(input_file, "r") as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            n = int(row[0])
            pdf = row[1]
            model = row[2]
            p = float(row[3])
            if row[4] == "None":
                q = None
            else:
                q = float(row[4])
            if row[5] == "None":
                num_grps = None
            else:
                num_grps = int(row[5])
            num_trials = int(row[6])
            X, Y = func([float(x) for x in row[7:]])
            key = (n, pdf, model, p, q, num_grps)
            if model == "Random Quarantine":
                string = f"q = {q}"
            elif model == "Scheduled Quarantine":
                string = f"Number of Groups = {num_grps}"
            else:
                string = None
            if key not in plots:
                plots[key] = default_plot(n, p, ylabel, num_trials, model, string)
            add_to_plot(plots[key], X, Y, plot_type, model, legend_label="", alpha=1)
    for key, plot in plots.items():
        n, pdf, model, p, q, num_grps = key
        plot.set_xlim(x_lim[key])
        plot.set_ylim(y_lim[key])
        fig = plot.get_figure()
        if not os.path.isdir(
            os.path.join(os.getcwd(), "output_files", "plots", model, str(p), "")
        ):
            os.makedirs(
                os.path.join(os.getcwd(), "output_files", "plots", model, str(p), "")
            )
        file_name = os.path.join(
            os.getcwd(),
            "output_files",
            "plots",
            model,
            str(p),
            f"{plot_type}_{n}_{pdf}_{model}_{p}_{q}_{num_grps}.png",
        )
        fig.savefig(file_name)
        plt.close(fig)


def overlaid_plots(plot_type, x_lim, y_lim):
    cwd = os.getcwd()
    ylabel, func = label_func(plot_type)
    input_file = os.path.join(cwd, "output_files", "csvs", "average_growth_data.csv")
    raw_data = dict()
    with open(input_file, "r") as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            n = int(row[0])
            pdf = row[1]
            model = row[2]
            p = float(row[3])
            if row[4] == "None":
                q = None
            else:
                q = float(row[4])
            if row[5] == "None":
                num_grps = None
            else:
                num_grps = int(row[5])
            num_trials = int(row[6])
            X, Y = func([float(x) for x in row[7:]])
            key = (n, pdf, model, p, q, num_grps, num_trials)
            raw_data[key] = (X, Y)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    p_values = set()
    q_values = set()
    grp_values = set()
    for n, pdf, model, p, q, num_grps, num_trials in raw_data:
        if q is not None:
            q_values.add(q)
        if num_grps is not None:
            grp_values.add(num_grps)
        p_values.add(p)
    keys = [
        (p, q, num_grps) for p in p_values for q in q_values for num_grps in grp_values
    ]
    if not os.path.isdir(os.path.join(cwd, "output_files", "plots", "overlaid", "")):
        os.mkdir(os.path.join(cwd, "output_files", "plots", "overlaid", ""))
    for new_key in keys:
        new_p, new_q, new_num_grps = new_key
        new_plot = default_plot(n, new_p, ylabel, num_trials)
        for key, (X, Y) in raw_data.items():
            n, pdf, model, p, q, num_grps, num_trials = key
            if new_p == p:
                if new_q == q and num_grps is None:
                    string = f"Random Quarantine (q = {q})"
                elif new_num_grps == num_grps and q is None:
                    string = f"Scheduled Quarantine (Number of groups = {num_grps})"
                elif q is None and num_grps is None:
                    string = model
                else:
                    continue
                add_to_plot(new_plot, X, Y, plot_type, model, string, alpha=1)
        x_lim[new_key] = new_plot.get_xlim()
        y_lim[new_key] = new_plot.get_ylim()
        if plot_type == "total":
            new_plot.legend(loc="lower right")
        else:
            new_plot.legend(loc="upper right")
        fig = new_plot.get_figure()
        file_name = os.path.join(
            cwd,
            "output_files",
            "plots",
            "overlaid",
            f"{plot_type}_{new_p}_{new_q}_{new_num_grps}.png",
        )
        fig.savefig(file_name)
        plt.close(fig)


def main():
    plot_types = ["new", "growth", "total"]
    x_lim, y_lim = defaultdict(int), defaultdict(int)
    for plot_type in plot_types:
        overlaid_plots(plot_type, x_lim, y_lim)
        individual_plots(plot_type, x_lim, y_lim)


if __name__ == "__main__":
    main()
