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

    if action in action_to_class:
        return action_to_class[action]

    answer = ask_class(action)
    return answer

def ask_class(action):
    """
    Asks user the classification of the given action.
    """
    while True:
        print(action)
        answer = input('Should the action above be classified W, R or N?: ')
        if answer in ['W', 'R', 'N']: # 'WRN' allows empty classification
            return answer

if __name__ == '__main__':
    atoc = import_action_to_class_dict()
    rtoc = import_regex_to_class_dict()
    c = classify_action(rtoc, atoc, 'f (asdf)')
    print(c)
