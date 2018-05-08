"""
This module classifies an action as Worthy, Rest, or Neither.
"""
import re

def import_regex_to_class_dict():
    """
    Imports regex-to-class dictionary from regex_to_class.csv.
    """
    regex_to_class = {}
    with open('regex_to_class.csv') as file:
        lines = file.readlines()
        for line in lines:
            regex, classification = line.strip().split(',')
            regex_to_class[regex] = classification

    return regex_to_class

def import_action_to_class_dict():
    """
    Imports action-to-class dictionary from action_to_class.csv.
    """
    action_to_class = {}
    with open('action_to_class.csv') as file:
        lines = file.readlines()
        for line in lines:
            action, classification = line.strip().split(',')
            action_to_class[action] = classification

    return action_to_class


def classify_action(regex_to_class, action_to_class, action):
    """
    Returns 'W', 'R', or 'N' if the given action is Worthy, Rest, or Neither.
    """
    for regex, classification in regex_to_class.items():
        if re.search(regex, action):
            return classification

    if action_to_class[action]:
        return action_to_class[action]

    return None

if __name__ == '__main__':
    atoc = import_action_to_class_dict()
    rtoc = import_regex_to_class_dict()
    c = classify_action(rtoc, atoc, 'Rest (asdf)')
    print(c)
