#!/usr/bin/env python3

import csv
import random

data = dict()
sample_size = dict()
with open("contact_distribution.csv") as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    for row in rows:
        country = row[0]
        number_of_participants = int(row[1])
        sample_size[country] = number_of_participants
        data[country] = [float(x) for x in row[2:]]


def contact_range(index, increment=2.5):
    lower = increment * index
    upper = increment * (index + 1)
    return (lower, upper)


def cdf(array):
    total = 0
    new_array = []
    for element in array:
        total += element
        new_array.append(total)
    return [t / total for t in new_array]


def pdf(array, increment=2.5):
    cumulative_distribution = cdf(array)

    def helper():
        p = random.uniform(0, 1)
        for i, total in enumerate(cumulative_distribution):
            if total >= p:
                if i == 0:
                    lower = 0
                else:
                    lower = cumulative_distribution[i - 1]
                upper = total
                return int((i + (p - lower) / (upper - lower)) * increment)

    return helper


be_pdf = pdf(data["BE"])
de_pdf = pdf(data["DE"])
fi_pdf = pdf(data["FI"])
gb_pdf = pdf(data["GB"])
it_pdf = pdf(data["IT"])
lu_pdf = pdf(data["LU"])
nl_pdf = pdf(data["NL"])
pl_pdf = pdf(data["PL"])
world_pdf = pdf(data["WORLD"])


def main():
    for _ in range(10):
        print(world_pdf())


if __name__ == "__main__":
    main()
