#!/usr/bin/env python3
"""
This module creates plots for the report using matplotlib.
"""
from matplotlib import pyplot

def pie_chart(filename, actions_list):
    """
    Draw a pie chart based on the given list of actions and saves it to a
    given filename.
    """
    # The slices will be ordered and plotted counter-clockwise
    labels = [action['label'] for action in actions_list]
    sizes = [action['duration'] for action in actions_list]

    _, ax1 = pyplot.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # Ensures that pie is drawn as a circle
    ax1.axis('equal')

    # Save figure
    pyplot.savefig('report/' + filename + '.png', bbox_inches='tight')
    pyplot.clf()

def create_plots(plot_data):
    """
    Create plots based on the given plot_data.
    """
    pie_chart(filename='daily_pie', actions_list=plot_data['summary'])
    pie_chart(filename='worthy_pie', actions_list=plot_data['worthy_list'])
    pie_chart(filename='neither_pie', actions_list=plot_data['neither_list'])
    pie_chart(filename='rest_pie', actions_list=plot_data['rest_list'])
