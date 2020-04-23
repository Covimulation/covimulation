#!/usr/bin/env python3

from collections import defaultdict
from mechanisms import model_string, model_label
import os
import csv


def merge_csvs(n, p_values, mechanisms, number_of_tests):
    model = model_string(mechanisms)
    output_file = os.path.join(
        os.getcwd(), "output_files", "csvs", f"growth_data_{n}_{model}.csv"
    )
    with open(output_file, "w") as output_csv:
        output_csv.write(f"n,p,days\n")
        for p in p_values:
            for i in range(number_of_tests):
                input_file = os.path.join(
                    os.getcwd(),
                    "output_files",
                    "csvs",
                    f"growth_data_{n}_{p:0.02f}_{model}_{i}.csv",
                )
                with open(input_file, "r") as input_csv:
                    for line in input_csv:
                        output_csv.write(line)
                os.remove(input_file)


def add_arrays(A, B):
    if len(A) > len(B):
        return [A[i] + B[i] for i in range(len(B))] + A[len(B) :]
    else:
        return [A[i] + B[i] for i in range(len(A))] + B[len(A) :]


def average_csvs(n, mechanisms):
    model = model_string(mechanisms)
    input_file = os.path.join(
        os.getcwd(), "output_files", "csvs", f"growth_data_{n}_{model}.csv"
    )
    output_file = os.path.join(
        os.getcwd(), "output_files", "csvs", f"average_growth_data_{n}_{model}.csv"
    )
    growth_rate = defaultdict(list)
    counts = defaultdict(int)
    with open(input_file, "r") as input_csv:
        reader = csv.reader(input_csv)
        next(reader)
        for row in reader:
            n = int(row[0])
            p = float(row[1])
            data = [int(x) for x in row[2:]]
            growth_rate[p] = add_arrays(growth_rate[p], data)
            counts[p] += 1
    with open(output_file, "w") as output_csv:
        days_string = ",".join([f"day {i}" for i in range(1, 2000)])
        output_csv.write(f"n,p,{days_string}\n")
        for p in growth_rate:
            growth_rate_string = ",".join([str(x / counts[p]) for x in growth_rate[p]])
            output_csv.write(f"{n},{p},{growth_rate_string}\n")


def csv_helper(n, p_values, mechanisms, number_of_tests):
    merge_csvs(n, p_values, mechanisms, number_of_tests)
    average_csvs(n, mechanisms)


def main():
    return 0


if __name__ == "__main__":
    main()
