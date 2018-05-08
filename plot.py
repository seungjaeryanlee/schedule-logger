#!/usr/bin/env python3
"""
This module creates plots for the report using matplotlib.
"""
from matplotlib import pyplot as plt
import matplotlib

MINIMUM_LABEL_PERCENT = 5

def create_plots(plot_data):
    """
    Create plots based on the given plot_data.
    """
    # Use font that has Korean letters
    matplotlib.rc('font', family='NanumGothic')

    create_summary_pie_chart(plot_data['summary_pie_chart'])

def create_summary_pie_chart(data, filename='summary'):
    """
    Creates a pie chart displaying the ratio of three classes 'W', 'R', and 'N'
    and saves the image to 'filename.png'.
    """
    # The slices will be ordered and plotted counter-clockwise
    labels = ['W', 'R', 'N']
    sizes = [data['class_duration'][label].seconds for label in labels]

    _, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct=autopct, startangle=90)
    # Ensures that pie is drawn as a circle
    ax1.axis('equal')

    # Save figure
    plt.savefig('report/' + filename + '.png', bbox_inches='tight')
    plt.clf()

def autopct(percent):
    """
    Custom autopct for pie charts that returns empty string if the percentage
    is too small.
    """
    if percent >= MINIMUM_LABEL_PERCENT:
        return '%.2f%%' % percent
    return ''
