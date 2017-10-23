#!/usr/bin/env python3
"""
This module creates a HTML report based on the data from the parsed file.
"""
import os
from jinja2 import Environment, FileSystemLoader

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
