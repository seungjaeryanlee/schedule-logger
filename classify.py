"""
This module classifies an action as Worthy, Rest, or Neither.
"""

def import_action_to_class_dict():
    """
    Imports action-to-class dictionary from action_to_class.csv
    """
    action_to_class = {}
    with open('action_to_class.csv') as file:
        lines = file.readlines()
        for line in lines:
            action, classification = line.strip().split(',')
            action_to_class[action] = classification

    print(action_to_class)
    return action_to_class


def classify_action(action_to_class, action):
    """
    Returns 'W', 'R', or 'N' if the given action is Worthy, Rest, or Neither.
    """

    return 'N'
