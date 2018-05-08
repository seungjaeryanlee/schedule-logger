#!/usr/bin/env python3
"""
This module creates a HTML report with plots by parsing data from the given
log file.
"""
import os
from sys import argv
from datetime import timedelta
from jinja2 import Environment, FileSystemLoader

from parse import Parser
from classify import Classifier
from plot import create_summary_pie_chart


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

def _render_template(template_filename, data):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(data)

def create_report(report_data):
    """
    Creates a report.html file in report/ directory using the template and
    given data.
    """
    # Create report/ directory if it doesn't exist
    if not os.path.exists('report/'):
        os.makedirs('report/')

    output_file = 'report/report.html'
    with open(output_file, 'w') as output:
        html = _render_template('template.html', report_data)
        output.write(html)


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
    create_report({ 'total_duration': total_duration })


if __name__ == '__main__':
    main()
