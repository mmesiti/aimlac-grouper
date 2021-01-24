#!/usr/bin/env python3
import pandas as pd
import numpy as np

index_columns = ["Name", "Surname"]
data_columns = ["Institution", "Theme", "Software Dev Expertise"]


def get_expertise_from_row(row):
    i = data_columns.index("Software Dev Expertise")
    return row[i]


def get_relevant_columns(filename="cohort.2020.csv"):
    df = pd.read_csv(filename)
    return df.loc[:, index_columns + data_columns]


def get_data_categoric(filename="cohort.2020.csv"):
    return get_relevant_columns(filename).set_index(index_columns)


def get_data_numeric(filename="cohort.2020.csv"):
    return unravel_data(get_relevant(filename))


def unravel_data(students_df):
    def reshape(df_students, prop):
        return (
            df_students[[*index_columns, prop]]
            .assign(idx=df_students.index)
            .assign(Value=1)
            .set_index([*index_columns, "idx", prop])
            .unstack(prop, fill_value=0)
            .groupby(index_columns)
            .mean()
        )

    themes = reshape(students_df, "Theme")
    institutions = reshape(students_df, "Institution")
    student_data = pd.concat([themes, institutions], axis="columns")

    return student_data, students_df


def show_groups(students, group_assignment):
    students_cp = pd.DataFrame(students).reset_index()
    students_cp["Group"] = group_assignment
    students_cp.set_index(*index_columns)
    print(students_cp.sort_values(by="Group"))


def get_students_group(students, group_assignment):
    return pd.Series(name="Group", index=students.index, data=group_assignment)
