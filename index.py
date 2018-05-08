#!/usr/bin/env python3
"""
This module parses a formatted file of activities throughout the day and
classifies each time partition as Worthy, Rest or Neither, and creates a report
from the data.
"""
import os.path
from sys import argv

from parse import parse_file
from plot import create_plots
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

    data = parse_file(argv[1])
    data['title'] = 'Daily Report'
    data['minutes_to_string'] = minutes_to_string

    create_plots(data)
    create_report(data)


if __name__ == '__main__':
    main()
