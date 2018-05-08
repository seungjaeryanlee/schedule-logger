#!/usr/bin/env python3
"""
This module creates plots for the report using matplotlib.
"""
from matplotlib import pyplot
import matplotlib
from datetime import timedelta

MINIMUM_LABEL_PERCENT = 5

def autopct(percent):
    """
    Custom autopct for pie charts that returns empty string if the percentage
    is too small.
    """
    if percent >= MINIMUM_LABEL_PERCENT:
        return '%.2f%%' % percent
    return ''

def pie_chart(filename, actions_list):
    """
    Draw a pie chart based on the given list of actions and saves it to a
    given filename.
    """
    # The slices will be ordered and plotted counter-clockwise
    labels = [action['label'] for action in actions_list]
    sizes = [action['duration'] for action in actions_list]

    # Erase label if too small
    sizes_sum = sum(sizes)
    for i, _ in enumerate(labels):
        percent = sizes[i] / sizes_sum * 100
        if percent < MINIMUM_LABEL_PERCENT:
            labels[i] = ''


    _, ax1 = pyplot.subplots()
    ax1.pie(sizes, labels=labels, autopct=autopct, startangle=90)
    # Ensures that pie is drawn as a circle
    ax1.axis('equal')

    # Save figure
    pyplot.savefig('report/' + filename + '.png', bbox_inches='tight')
    pyplot.clf()

def create_plots(plot_data):
    """
    Create plots based on the given plot_data.
    """
    # Use font that has Korean letters
    matplotlib.rc('font', family='NanumGothic')

    pie_chart(filename='daily_pie', actions_list=plot_data['summary'])
    pie_chart(filename='worthy_pie', actions_list=plot_data['worthy_list'])
    pie_chart(filename='neither_pie', actions_list=plot_data['neither_list'])
    pie_chart(filename='rest_pie', actions_list=plot_data['rest_list'])

def create_summary_pie_chart(data, filename='summary'):
    """
    Creates a pie chart displaying the ratio of three classes 'W', 'R', and 'N'
    and saves the image to 'filename.png'.
    """
    # The slices will be ordered and plotted counter-clockwise
    labels = ['W', 'R', 'N']
    sizes = [data['class_duration'][label].seconds for label in labels]

    _, ax1 = pyplot.subplots()
    ax1.pie(sizes, labels=labels, autopct=autopct, startangle=90)
    # Ensures that pie is drawn as a circle
    ax1.axis('equal')

    # Save figure
    pyplot.savefig('report/' + filename + '.png', bbox_inches='tight')
    pyplot.clf()
