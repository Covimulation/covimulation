#!/usr/bin/env python3

import random
from collections import defaultdict


def vose_alias_method_sampler(weights, keys=None):
    n = len(weights)
    total = sum(weights)
    weighted_probs = [n * weight / total for weight in weights]
    Alias = [None for _ in range(n)]
    Prob = [None for _ in range(n)]
    Small, Large = [], []
    for i, p in enumerate(weighted_probs):
        if p < 1:
            Small.append(i)
        else:
            Large.append(i)
    while Small and Large:
        l = Small.pop(0)
        g = Large.pop(0)
        Prob[l] = weighted_probs[l]
        Alias[l] = g
        weighted_probs[g] += weighted_probs[l] - 1
        if weighted_probs[g] < 1:
            Small.append(g)
        else:
            Large.append(g)
    for g in Large:
        Prob[g] = 1
    for l in Small:
        Prob[l] = 1

    def sampler_index():
        i = random.randint(0, n - 1)
        coin_toss = random.uniform(0, 1)
        if coin_toss < Prob[i]:
            return i
        else:
            return Alias[i]

    if keys is None:
        return sampler_index
    else:

        def sampler():
            i = sampler_index()
            return keys[i]

        return sampler


def vose_sample_with_replacement(k, weights, keys=None):
    sampler = vose_alias_method_sampler(weights, keys)
    return [sampler() for _ in range(k)]


def vose_sample_without_replacement(k, weights, keys=None, skip=None):
    sampler = vose_alias_method_sampler(weights, keys)
    if skip is None:
        seen = set()
    else:
        seen = set(skip)
    result = []
    for _ in range(k):
        sample = sampler()
        while sample in seen:
            sample = sampler()
        result.append(sample)
        seen.add(sample)
    return result


def sample_without_replacement(k, pdf, skip=None):
    if skip is None:
        seen = set()
    else:
        seen = set(skip)
    result = []
    for _ in range(k):
        sample = pdf()
        while sample in seen:
            sample = pdf()
        result.append(sample)
        seen.add(sample)
    return result


def main():
    values = list(range(10))
    weights = [random.randint(1, 100) for _ in range(10)]
    total = sum(weights)
    sample_data = defaultdict(int)
    real_data = {value: weight / total for value, weight in zip(values, weights)}
    test_function = vose_alias_method_sampler(weights, values)
    for _ in range(10 ** 9):
        value = test_function()
        sample_data[value] += 1
    for key in sample_data:
        sample_data[key] /= 10 ** 9
    for value in values:
        print(abs(real_data[value] - sample_data[value]))


if __name__ == "__main__":
    main()
