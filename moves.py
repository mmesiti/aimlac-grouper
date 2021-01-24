#!/usr/bin/env python3
import numpy as np

def swap2students(group_assignment):
    nstudents = group_assignment.shape[0]
    s1 = 0
    s2 = 0

    while s1 == s2 or group_assignment[s1] == group_assignment[s2]:
        s1 = np.random.randint(nstudents)
        s2 = np.random.randint(nstudents)

    new_group_assignment = np.array(group_assignment)
    new_group_assignment[s1] = group_assignment[s2]
    new_group_assignment[s2] = group_assignment[s1]
    return new_group_assignment


def move_student(group_assignment, ngroups):
    nstudents = group_assignment.shape[0]
    new_group_assignment = np.array(group_assignment)

    s = np.random.randint(nstudents)
    new_group_assignment[s] = group_assignment[s]
    while new_group_assignment[s] == group_assignment[s]:
        new_group_assignment[s] = np.random.randint(ngroups)

    return new_group_assignment


def new_assignment(group_assignment, ngroups):

    if np.random.uniform() > 0.2 and np.any(np.diff(group_assignment) != 0):
        return swap2students(group_assignment)
    else:
        return move_student(group_assignment, ngroups)


def random_assignment(nstudents, ngroups):
    return np.random.randint(low=0, high=ngroups, size=nstudents)
