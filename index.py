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
    create_plots(data)
    create_report(data)


if __name__ == '__main__':
    main()
