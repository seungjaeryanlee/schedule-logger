#!/usr/bin/python3
"""
This module creates plots for the report using matplotlib.
"""
from matplotlib import pyplot

def plot_daily_pie(plot_data):
    """
    Draw a pie chart of daily activities, categorized by Worthy, Rest, and
    Neither.
    """
    # The slices will be ordered and plotted counter-clockwise
    labels = 'Worthy', 'Rest', 'Neither'
    sizes = plot_data['daily'] # in percentage

    _, ax1 = pyplot.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # Ensures that pie is drawn as a circle
    ax1.axis('equal')

    # Save figure
    pyplot.savefig('report/daily_pie.png', bbox_inches='tight')
    pyplot.clf()

def create_plots(plot_data):
    """
    Create plots based on the given plot_data.
    """
    plot_daily_pie(plot_data)
