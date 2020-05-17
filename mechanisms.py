#!/usr/bin/env python3

mechanisms = [None, "random quarantine", "symptomatic quarantine", "scheduled quarantine"]


def model_string(mechanism):
    if mechanism is None:
        return "basic_model"
    else:
        return mechanism.replace(" ", "_")


def model_label(mechanism):
    if mechanism is None:
        return "Basic Model"
    else:
        return mechanism.title()
