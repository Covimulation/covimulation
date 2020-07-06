#!/usr/bin/env python3

import csv
import random
import matplotlib.pyplot as plt

data = dict()
sample_size = dict()
with open("contact_distribution.csv") as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    for row in rows:
        country = row[0]
        sample_size[country] = int(row[1])
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

be_pdf.__name__ = "be_pdf"
de_pdf.__name__ = "de_pdf"
fi_pdf.__name__ = "fi_pdf"
gb_pdf.__name__ = "gb_pdf"
it_pdf.__name__ = "it_pdf"
lu_pdf.__name__ = "lu_pdf"
nl_pdf.__name__ = "nl_pdf"
pl_pdf.__name__ = "pl_pdf"
world_pdf.__name__ = "world_pdf"


def main():
    data = [world_pdf() for _ in range(50000)]
    plt.hist(data, bins=50)
    plt.xticks(range(0, 50, 5))
    plt.show()
    return 0


if __name__ == "__main__":
    main()
