import numpy as np
import pandas as pd

"""
Module for parsing and formatting csv files
"""

class Dancer:
    """
    Class representing a dancer
    """
    def __init__(self, name, email, dances, preferences):
        self.name = name
        self.email = email
        self.dances = dances
        self.preferences = preferences
    
    def __str__(self):
        return f"{self.name} [{self.email}] ({self.dances} dances): {', '.join(self.preferences)}"


class Dance:
    """
    Class representing a dance
    """
    def __init__(self, name, max_capacity):
        self.name = name
        self.max_capacity = max_capacity
    
    def __str__(self):
        return f"{self.name} [max capacity: {self.max_capacity}]"


def parse_preferences(csv_path: str) -> list[Dancer]:
    """
    Parses a preferences file and returns a list of preferences.
    """
    dancers = []
    df = pd.read_csv(csv_path)
    df.rename(columns={"How many dances would you like to join?": "Dances"}, inplace=True)

    for index, row in df.iterrows():
        preferences = row[3:].dropna().tolist()
        dancer = Dancer(name=row["Full Name"], email=row["Email Address"], dances=int(row["Dances"]), preferences=preferences)
        dancers.append(dancer)

    return dancers


def parse_dances(csv_path: str) -> list[Dance]:
    """
    Parses a dances file and returns a list of dances.
    """
    dances = []
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        dance = Dance(row["Dance Name"], row["Max Capacity"])
        dances.append(dance)
    return dances