#!/usr/bin/env python3
"""
This module parses a formatted file of activities throughout the day and
classifies each time partition as Worthy, Rest or Neither, and creates a report
from the data.
"""
import os.path
from sys import argv
from datetime import timedelta

from parse import parse_file, Parser
from classify import Classifier
from plot import create_plots, create_summary_pie_chart
from report import create_report

def minutes_to_string(minutes):
    """
    Returns '0h', '0m' or '0h 0m' formatted string from given minutes (int).
    """
    if minutes // 60 == 0:
        return str(minutes % 60) + 'm'
    elif minutes % 60 == 0:
        return str(minutes // 60) + 'h'

    return str(minutes // 60) + 'h ' + str(minutes % 60) + 'm'

def main():
    """
    Only run when this module is run directly
    """
    if len(argv) == 1:
        print('No argument specified.')
        quit()
    if len(argv) == 3:
        print('Too many arguments specified.')
        quit()
    if not os.path.exists(argv[1]):
        print('No such file exists')
        quit()

    # data = parse_file(argv[1])
    # data['title'] = 'Daily Report'
    # data['minutes_to_string'] = minutes_to_string

    # create_plots(data)
    # create_report(data)

    parser = Parser()
    classifier = Classifier()

    activities = parser.parse_file(argv[1])
    total_duration = {
        'W': timedelta(hours=0, minutes=0),
        'R': timedelta(hours=0, minutes=0),
        'N': timedelta(hours=0, minutes=0),
    }
    
    for activity in activities:
        duration = activity['duration']
        actions = activity['actions']
        divided_duration = duration / len(actions)

        for action in actions:
            classification = classifier.classify_action(action)
            total_duration[classification] += divided_duration

    create_summary_pie_chart(total_duration)


if __name__ == '__main__':
    main()
