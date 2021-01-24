#!/usr/bin/env python3
import numpy as np


def team_cost(selection, binary_cost):
    cost = 0
    for s1 in range(selection.shape[0]):
        for s2 in range(s1 + 1, selection.shape[0]):
            cost += binary_cost(selection[s1, :], selection[s2, :])

    return cost


def get_cost(
    student_data_values,
    team_assignment,
    nteams,
    binary_cost,
    global_cost_factors,
    get_expertise,
):
    cost = 0
    team_sizes = []
    team_expertises = []
    for i in range(nteams):
        selection = student_data_values[team_assignment == i, :]
        cost += team_cost(selection, binary_cost)

        # size
        team_sizes.append(len(selection))

        # expertise
        team_expertises.append(sum(get_expertise(s) for s in selection))

    cost += np.var(team_sizes) * global_cost_factors["team_size_imbalance"]
    cost += np.var(team_expertises) * global_cost_factors["team_expertise_imbalance"]

    return cost


def binary_cost_mixed(sd1, sd2, ncategorical, weights):
    """
    First `ncategorical` variables in sd1 and sd2
    are going to be categorical, the rest numeric.

    len(sd1) == len(sd2) == len(weights)
    """
    cost = 0
    for i, (attrs1, attrs2, w) in enumerate(zip(sd1, sd2, weights)):
        if i < ncategorical:
            a1 = set(str(attrs1).split(","))
            a2 = set(str(attrs2).split(","))

            cost += w * len(set.intersection(a1, a2)) / len(set.union(a1, a2))
        else:
            cost += w * (attrs1 - attrs2) ** 2
    return cost
