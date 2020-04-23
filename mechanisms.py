#!/usr/bin/env python3

mechanism_1 = "random quarantine"
mechanism_2 = "symptomatic quarantine"
mechanism_4 = "scheduled quarantine"

Mechanisms = [
    (),
    (mechanism_1,),
    (mechanism_2,),
    (mechanism_1, mechanism_2),
    (mechanism_1, mechanism_4),
    (mechanism_2, mechanism_4),
    (mechanism_1, mechanism_2, mechanism_4),
]


def model_string(mechanisms):
    if mechanisms:
        return "_".join(sorted(list(mechanisms))).replace(" ", "_")
    else:
        return "basic_model"


def model_label(mechanisms):
    labels = []
    if mechanism_1 in mechanisms:
        labels.append("Random")
    if mechanism_2 in mechanisms:
        labels.append("Symptomatic")
    if mechanism_4 in mechanisms:
        labels.append("Scheduled")
    labels.sort()
    if labels:
        return f"{', '.join(labels)} Quarantine Model"
    else:
        return "Basic Model"
