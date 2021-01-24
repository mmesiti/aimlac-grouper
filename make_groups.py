#!/usr/bin/env python3
from data import (
    get_data_categoric,
    get_relevant_columns,
    get_students_group,
    get_expertise_from_row,
)
from moves import random_assignment, new_assignment
from cost import get_cost, binary_cost_mixed

from sys import argv, stderr
import numpy as np
import pandas as pd


ngroups = int(argv[1])
try:
    datafile = argv[2]
except:
    datafile = "cohort.2020.csv"

students_df = get_relevant_columns(datafile)
student_data = get_data_categoric(datafile)
nsteps = 10000

values = student_data.values

# YOUR SETTINGS HERE


def binary_cost(s1, s2):
    """
    Cost associated to the pairs of students.
    """
    different_institution_weight = 1.5
    different_theme_weight = 1.5
    different_expertise_weight = 1.5
    weights = [
        different_institution_weight,
        different_theme_weight,
        different_expertise_weight,
    ]
    return binary_cost_mixed(s1, s2, ncategorical=3, weights=weights)


global_cost_factors = dict(team_size_imbalance=10, team_expertise_imbalance=10)


def temperature(step):
    return 1000 * 2 ** (-step / 300) + 1000 / (1 + step)


# END OF SETTINGS

group_assignment = random_assignment(len(student_data), ngroups)
cost = get_cost(
    values,
    group_assignment,
    ngroups,
    binary_cost,
    global_cost_factors,
    get_expertise_from_row,
)

log_data = []
for step in range(nsteps):
    new_group_assignment = new_assignment(group_assignment, ngroups)
    new_cost = get_cost(
        values,
        new_group_assignment,
        ngroups,
        binary_cost,
        global_cost_factors,
        get_expertise_from_row,
    )

    probability = min(1, np.exp(-(new_cost - cost) / temperature(step)))

    log_data_row = [step, new_cost, cost, probability, temperature(step)]

    if np.random.uniform() < probability:
        group_assignment = new_group_assignment
        cost = new_cost
        log_data_row.append(1)
    else:
        log_data_row.append(0)
    log_data.append(log_data_row)
    if step % 50 == 0:
        message = f"Step:{step} - cost:{cost:1.5e}\r"
        stderr.write(message)
stderr.write("\n")


log_data = pd.DataFrame(
    data=log_data,
    columns=["steps", "new_cost", "cost", "probability", "temperature", "accepted"],
)
assert len(log_data.columns) == 6

log_data.to_csv("log_data.csv")


students_groups = (
    get_students_group(student_data, group_assignment).to_frame().reset_index()  #  #  #
)
print(
    pd.merge(students_groups, students_df, on=["Name", "Surname"]).sort_values(
        by=["Group", "Institution", "Theme", "Software Dev Expertise"]
    )
)


def plot():
    from matplotlib import pyplot as plt

    log_data.cost.plot(title="Evolution of cost function", label="cost function")
    window = 100
    (log_data.accepted * max(log_data.cost)).rolling(window=window).mean().plot(
        label=f"acceptance - rolling avg ({window}) - arbitrary scale"
    )
    (log_data.temperature * max(log_data.cost) / max(log_data.temperature)).plot(
        label=f"temperature - arbitrary scale"
    )
    plt.ylim([0, None])
    plt.legend()
    plt.show()

try:
    plot()
except:
    stderr.write("Plot failed\n")
