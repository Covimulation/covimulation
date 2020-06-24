#!/usr/bin/env python3

import matplotlib.pyplot as plt
import csv
from mechanisms import mechanisms, model_string, model_label
import os
import sys
from collections import defaultdict
from itertools import product
import re

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


def add_to_plot(plot, X, Y, plot_type, model, label="", alpha=1):
    color = colors[model]
    if plot_type == "growth":
        plot.plot(X, Y, label=label, alpha=alpha, color=color)
    else:
        plot.scatter(X, Y, label=label, alpha=alpha, color=color)


def default_plot(n, T_p, q, ylabel, t, pdf, model, schedule):
    _, plot = plt.subplots(figsize=(16, 9))
    m_string = ""
    if model == "Random Quarantine":
        m_string = f"{100 * q:0.2f}% of population quarantined"
    elif model == "Scheduled Quarantine":
        m_string = f"Schedule of {schedule}"
    plot.set_xlabel("Day")
    plot.set_ylabel(ylabel)
    plot.set_title(
        f"""{ylabel} with n = {n}, T_p = {T_p:0.2f}
            (Average over {t} Simulations)
            Contact Distribution = {pdf}
            {model}
            {m_string}"""
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


def legend_sort(label):
    if label == "Basic Model":
        return 0
    elif label == "Symptomatic Quarantine":
        return 1
    elif label.split(" ")[-1] == "quarantined":
        return 2
    else:
        return 3


def individual_plots(plot_type, x_lim, y_lim):
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
            p = float(row[2])
            model = row[3]
            T_p = float(row[4])
            if row[5] != "None":
                q = float(row[5])
            else:
                q = None
            if row[6] != "None":
                k = int(row[6])
            else:
                k = None
            if row[7] != "None":
                schedule = row[7]
            else:
                schedule = None
            t = int(row[8])
            X, Y = data_func([float(x) for x in row[9:]])
            plot = default_plot(n, p, q, ylabel, t, pdf, None, schedule)
            sched_key = (k, schedule)
            key = (n, pdf, p, q, T_p, q, sched_key)
            add_to_plot(plot, X, Y, plot_type, model)
            plot.set_xlim(x_lim[(n, p, q, pdf, model)])
            plot.set_ylim(y_lim[(n, p, q, pdf, model)])
            fig = plot.get_figure()
            if q:
                q_str = f"{q:0.02f}"
            else:
                q_str = None
            file_name = os.path.join(
                os.getcwd(),
                "output_files",
                "plots",
                f"{n}_{p:0.2f}_{pdf}_{T_p:0.02f}_{q_str}_{sched_key}_{plot_type}.png",
            )
            fig.savefig(file_name)
            plt.close(fig)


def overlaid_plots(plot_type, x_lim, y_lim):
    ylabel, data_func = label_func(plot_type)
    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    input_file = os.path.join(
        os.getcwd(), "output_files", "csvs", f"average_growth_data.csv"
    )
    n_values = set()
    pdfs = set()
    p_values = set()
    models = set()
    Tp_values = set()
    q_values = set()
    sched_keys = set()
    plots = dict()
    data = dict()
    with open(input_file, "r") as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            n = int(row[0])
            pdf = row[1]
            p = float(row[2])
            model = row[3]
            T_p = float(row[4])
            if row[5] != "None":
                q = float(row[5])
            else:
                q = None
            if row[6] != "None":
                k = int(row[6])
            else:
                k = None
            if row[7] != "None":
                schedule = row[7]
            else:
                schedule = None
            n_values.add(n)
            pdfs.add(pdf)
            p_values.add(p)
            models.add(model)
            Tp_values.add(T_p)
            q_values.add(q)
            sched_keys.add((k, schedule))
            t = int(row[8])
            X, Y = data_func([float(x) for x in row[9:]])
            data_key = (n, pdf, p, model, T_p, q, k, schedule)
            data[data_key] = (X, Y)
    q_values.remove(None)
    sched_keys.remove((None, None))
    for key in product(n_values, pdfs, p_values, Tp_values, q_values, sched_keys):
        n, pdf, p, T_p, q, sched_key = key
        plots[key] = default_plot(n, T_p, q, ylabel, 10, pdf, "", "")
    for n, pdf, p, model, T_p, q, k, schedule in data:
        X, Y = data[(n, pdf, p, model, T_p, q, k, schedule)]
        if model == "Basic Model":
            for key in plots:
                plot_n, plot_pdf, plot_p, plot_T_p, plot_q, plot_sched_key = key
                plot_k, plot_schedule = plot_sched_key
                if all([n == plot_n, pdf == plot_pdf, p == plot_p, T_p == plot_T_p,]):
                    add_to_plot(plots[key], X, Y, plot_type, model, model, alpha=0.7)
        elif model == "Random Quarantine":
            for key in plots:
                plot_n, plot_pdf, plot_p, plot_T_p, plot_q, plot_sched_key = key
                plot_k, plot_schedule = plot_sched_key
                if all(
                    [
                        n == plot_n,
                        pdf == plot_pdf,
                        p == plot_p,
                        T_p == plot_T_p,
                        q == plot_q,
                    ]
                ):
                    label = f"{100 * q:0.2f}% of population quarantined"
                    add_to_plot(plots[key], X, Y, plot_type, model, label, alpha=0.7)
        elif model == "Symptomatic Quarantine":
            for key in plots:
                plot_n, plot_pdf, plot_p, plot_T_p, plot_q, plot_sched_key = key
                plot_k, plot_schedule = plot_sched_key
                if all([n == plot_n, pdf == plot_pdf, p == plot_p, T_p == plot_T_p,]):
                    add_to_plot(plots[key], X, Y, plot_type, model, model, alpha=0.7)
        elif model == "Scheduled Quarantine":
            for key in plots:
                plot_n, plot_pdf, plot_p, plot_T_p, plot_q, plot_sched_key = key
                plot_k, plot_schedule = plot_sched_key
                if all(
                    [
                        n == plot_n,
                        pdf == plot_pdf,
                        p == plot_p,
                        T_p == plot_T_p,
                        k == plot_k,
                        schedule == plot_schedule,
                    ]
                ):
                    label = f"{k} groups - {schedule}"
                    add_to_plot(plots[key], X, Y, plot_type, model, label, alpha=0.7)

    if not os.path.isdir(os.path.join(os.getcwd(), "output_files", "plots", "")):
        os.mkdir(os.path.join(os.getcwd(), "output_files", "plots", ""))
    for key, plot in plots.items():
        n, pdf, p, T_p, q, sched_key = key
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
            f"{n}_{p:0.2f}_{pdf}_{T_p:0.02f}_{q:0.02f}_{sched_key}_{plot_type}.png",
        )
        handles, labels = plot.get_legend_handles_labels()
        plot.legend(
            *zip(
                *sorted(
                    zip(*plot.get_legend_handles_labels()), key=lambda s: legend_sort(s[1])
                )
            )
        )
        fig.savefig(file_name)
        plt.close(fig)


def plot_helper():
    plot_types = ["new", "growth", "total"]
    x_lim, y_lim = defaultdict(int), defaultdict(int)
    for plot_type in plot_types:
        overlaid_plots(plot_type, x_lim, y_lim)
        # individual_plots(plot_type, x_lim, y_lim)


def main():
    plot_helper()


if __name__ == "__main__":
    main()
