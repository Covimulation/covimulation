#!/usr/bin/env python3

mechanism_1 = "random quarantine"
mechanism_2 = "symptomatic quarantine"
mechanism_4 = "scheduled quarantine"

Mechanisms = [(), (mechanism_1,), (mechanism_2,), (mechanism_2, mechanism_4)]


def model_string(mechanisms):
    if mechanisms:
        return "_".join(sorted(list(mechanisms))).replace(" ", "_")
    else:
        return "basic_model"


def model_label(mechanisms):
    if mechanisms == ():
        return "Basic Model"
    elif mechanisms == (mechanism_1,):
        return "Random Quarantine"
    elif mechanisms == (mechanism_2,):
        return "Symptomatic Quarantine"
    elif mechanisms == (mechanism_2, mechanism_4):
        return "Scheduled Quarantine"
