#!/usr/bin/env python

import os
import sys
import math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import SimpleLineChart, StackedHorizontalBarChart, StackedVerticalBarChart, \
    GroupedHorizontalBarChart, GroupedVerticalBarChart

import settings

def stacked_horizontal():
    chart = StackedHorizontalBarChart(400, 200,
                                      x_range=(0, 35))
    chart.set_bar_width(10)
    chart.set_colours(['00ff00', 'ff0000','ACff0C','B0ffE0','C0ffFF'])
    chart.add_data([1,2,3,4,5])
    chart.set_title('This is title')
    chart.set_legend( ['a','b','c','d','e'])
    chart.set_axis_labels('y', ['aa','bb','cc','dd','ee'])
    chart.annotated_data()
    chart.download('bar-horizontal-stacked.png')

def simple_line():
    chart = SimpleLineChart(settings.width, settings.height,
                                      x_range=(0, 35))
    chart.set_colours(['00ff00', 'ff0000','ACff0C','B0ffE0','C0ffFF'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.set_title('This is title')
    chart.set_axis_labels('r', 'str')
    chart.set_legend( ['a','b','c','d','e'])
    chart.download('simple-line.png')

def stacked_vertical():
    chart = StackedVerticalBarChart(settings.width, settings.height,
                                    y_range=(0, 35))
    chart.set_bar_width(10)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-vertical-stacked.png')

def grouped_horizontal():
    chart = GroupedHorizontalBarChart(settings.width, settings.height,
                                      x_range=(0, 35))
    chart.set_bar_width(5)
    chart.set_bar_spacing(2)
    chart.set_group_spacing(4)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-horizontal-grouped.png')

def grouped_vertical():
    chart = GroupedVerticalBarChart(settings.width, settings.height,
                                    y_range=(0, 35))
    chart.set_bar_width(5)
    chart.set_colours(['00ff00', 'ff0000'])
    chart.add_data([1,2,3,4,5])
    chart.add_data([1,4,9,16,25])
    chart.download('bar-vertical-grouped.png')


def main():
    stacked_horizontal()
    stacked_vertical()
    grouped_horizontal()
    grouped_vertical()
    simple_line()

if __name__ == '__main__':
    stacked_horizontal()
    #main()

