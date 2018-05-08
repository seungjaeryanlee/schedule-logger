"""
This module defines the Classifier class which classifies an action as
Worthy, Rest, or Neither.
"""
import re

class Classifier:
    """
    Classifier can clasisfy given action as Worthy, Rest, or Neither.
    """
    def __init__(self):
        """
        Import dictionaries from CSV files.
        """
        self.regex_to_class = self.import_regex_to_class_dict()
        self.action_to_class = self.import_action_to_class_dict()

    def import_regex_to_class_dict(self):
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

    def import_action_to_class_dict(self):
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

    def classify_action(self, action):
        """
        Returns 'W', 'R', or 'N' if the given action is Worthy, Rest, or Neither.
        """
        for regex, classification in self.regex_to_class.items():
            if re.search(regex, action):
                return classification

        if action in self.action_to_class:
            return self.action_to_class[action]

        answer = self.ask_class(action)
        return answer

    def ask_class(self, action):
        """
        Asks user the classification of the given action.
        """
        while True:
            print(action)
            answer = input('Should the action above be classified W, R or N?: ')
            if answer in ['W', 'R', 'N']: # 'WRN' allows empty classification
                self.append_action_to_class_dict(action, answer)
                return answer

    def append_action_to_class_dict(self, action, classification):
        """
        Append new (action, classification) pair to action_to_class dictionary.
        """
        # Update local dictionary
        self.action_to_class[action] = classification
        
        # Update file
        with open('action_to_class.csv', 'a+') as file:
            file.write('\n{},{}'.format(action, classification))
