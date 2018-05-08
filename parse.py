#!/usr/bin/env python3
"""
This module parses a formatted file of activities throughout the day and
classifies each time partition as Worthy, Neither or Rest.
"""
from datetime import timedelta

class Parser:
    """
    A file parser that returns a dictionary with information.
    """
    def __init__(self):
        pass

    def parse_file(self, filename):
        """
        Parses the file with given filename and returns a dictionary with info
        of classification of actions in the file.
        """
        lines = self.preprocess_file(filename)
        parsed_list = self.parse_lines(lines)

        return parsed_list

    @staticmethod
    def preprocess_file(filename):
        """
        Preprocesses specified file and returns list of lines.
        """
        with open(filename, encoding='utf-8') as input_file:
            lines = input_file.readlines()
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line[0] != '#']

        return lines

    def parse_lines(self, lines):
        """
        Parses the given list of lines and returns a dictionary with info
        of classification of actions in the lines.
        """
        parsed_list = []
        last_timestamp = timedelta(hours=0, minutes=0)
        is_pm = False
        for line in lines:
            if line == '~':
                is_pm = True
                continue

            timestamp, actions = self.parse_line(line, is_pm)
            parsed_list.append({
                'start_time': last_timestamp,
                'end_time': timestamp,
                'duration': timestamp - last_timestamp,
                'actions': actions
            })
            last_timestamp = timestamp

        return parsed_list

    def parse_line(self, line, is_pm):
        """
        Parses the given line and returns a dictionary with classification
        of the line.
        """
        timestamp, actions = line[0:5], line[5:].split('/')
        timestamp = self.string_to_timedelta(timestamp.strip(), is_pm)
        actions = [action.strip() for action in actions]

        return (timestamp, actions)

    @staticmethod
    def string_to_timedelta(string, is_pm):
        """
        Converts string-type timestamp to timedelta-type timestamp.

        Examples
        --------
        string_to_timedelta('000') == timedelta(hours=0, minutes=0)
        string_to_timedelta('030') == timedelta(hours=0, minutes=30)
        string_to_timedelta('100') == timedelta(hours=1, minutes=0)
        string_to_timedelta('1200') == timedelta(hours=12, minutes=0)
        """
        if len(string) == 3:
            hours = int(string[0])
            minutes = int(string[1:3])
        elif len(string) == 4:
            hours = int(string[0:2])
            minutes = int(string[2:4])

        if is_pm:
            hours += 12

        return timedelta(hours=hours, minutes=minutes)
