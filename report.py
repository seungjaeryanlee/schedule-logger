#!/usr/bin/env python3
"""
This module creates a HTML report with plots by parsing data from the given
log file.
"""
import os
from sys import argv
from datetime import timedelta
from jinja2 import Environment, FileSystemLoader

from classify import Classifier
from parse import Parser
from plot import create_plots


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


def timedelta_to_string(timestamp):
    """
    Returns '0h', '0m' or '0h 0m' formatted string from given timedelta-type
    timestamp.
    """
    if timestamp.seconds // 3600 == 0:
        return str(timestamp.seconds // 60 % 60) + 'm'
    elif timestamp.seconds // 60 % 60 == 0:
        return str(timestamp.seconds // 3600) + 'h'

    return '{}h {}m'.format(str(timestamp.seconds // 3600),
                            str(timestamp.seconds // 60 % 60))

def prepare_data(filename):
    """
    Parse and classify text from file with given filename to prepare data to
    generate the report.
    """
    parser = Parser()
    classifier = Classifier()

    class_duration = {    # Dictionary for duration of each class
        'W': timedelta(hours=0, minutes=0),
        'R': timedelta(hours=0, minutes=0),
        'N': timedelta(hours=0, minutes=0),
    }
    action_durations = {} # Dictionary for duration of each action

    activities = parser.parse_file(filename)
    for activity in activities:
        duration = activity['duration']
        actions = activity['actions']

        divided_duration = duration / len(actions)
        for action in actions:
            classification = classifier.classify_action(action)
            class_duration[classification] += divided_duration
            if action in action_durations:
                action_durations[action] += divided_duration
            else:
                action_durations[action] = divided_duration

    sorted_action_durations = sorted(action_durations.items(),
                                     key=lambda tup: tup[1], reverse=True)

    # Add structure to data and return
    plot_data = {
        'summary_pie_chart': {
            'class_duration': class_duration,
        },
    }
    report_data = {
        'sorted_action_durations': sorted_action_durations,
        'class_duration': class_duration,
        'timedelta_to_string': timedelta_to_string,
    }
    return plot_data, report_data

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

    plot_data, report_data = prepare_data(argv[1])

    create_plots(plot_data)
    create_report(report_data)


if __name__ == '__main__':
    main()
