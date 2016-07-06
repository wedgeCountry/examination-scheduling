#!/usr/bin/env python
# -*- coding: utf-8 -*-

# In this file we can find every functions concerning the visualization
# The principal function make a visualisation for two variable: x[i, k] and y[i, l]
# i=exam, k=room, l=period
# If we have an other variable, we transform it to both variables above

import os
import sys
PATHS = os.getcwd().split('/')
PROJECT_PATH = ''
for p in PATHS:
    PROJECT_PATH += '%s/' % p
    if p == 'examination-scheduling':
        break
sys.path.append(PROJECT_PATH)

import csv
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from scipy.optimize import brentq

from inputData import tools as csvtools


def get_colors():
    
    # These are the "Tableau 20" colors as RGB.
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 187, 120), (255, 127, 14),
                (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
    
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)
    
    return tableau20

def prepare_axes(ax, x_min, x_max, y_min, y_max):
    
    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    
    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
        
    # Limit the range of the plot to only where the data is.
    # Avoid unnecessary whitespace.
    plt.ylim(y_min, y_max)
    plt.xlim(x_min, x_max)
    # Make sure your axis ticks are large enough to be easily read.
    # You don't want your viewers squinting to read your plot.
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    
    ## Remove the tick marks; they are unnecessary with the tick lines we just plotted.
    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                    labelbottom="on", left="off", right="off", labelleft="on")

plotdir = "%svisualization/plots/" %PROJECT_PATH
datadir = "%svisualization/data/" %PROJECT_PATH
    

f1 = lambda x: (x-5.5)**2 - 0.1*x**4 + (x+5)**2 + 2*x - 45

leftroot = brentq(f1, -6, -2)
rightroot = brentq(f1, 2, 6)

x_vals = np.linspace(leftroot, rightroot, num=100)

fs = [f1] + [ lambda x: np.exp(0.3*f1(x)), lambda x: np.exp(0.6*f1(x)) ]

values = [ f(x_vals)/integrate.quad(f, leftroot, rightroot)[0] for f in fs ]

x_min, x_max = leftroot, rightroot
y_min, y_max = min( min(y) for y in values ) - 0.1, max( max(y) for y in values ) + 0.1

# You typically want your plot to be ~1.33x wider than tall. This plot is a rare
# exception because of the number of lines being plotted on it.
# Common sizes: (10, 7.5) and (12, 9)
plt.figure(figsize=(12, 9))

# prepare axes 
ax = plt.subplot(111)
prepare_axes(ax, x_min, x_max, y_min, y_max)

#set title
plt.title("Simulated Annealing")

# plot each line
colors = get_colors()
counter = 0
for rank, y_vals in enumerate(values):
    #ax.bar(x_vals, y_vals, lw=2.5, color=colors[rank])
    plt.plot(x_vals, y_vals, lw=2.5, color=colors[rank])
    plt.savefig("%sannealing_plot_%d.png" %(plotdir, counter), bbox_inches="tight");
    counter += 1

plt.clf()
plt.figure(figsize=(12, 9))

# prepare axes 
ax = plt.subplot(111)
prepare_axes(ax, x_min, x_max, y_min, max(values[1]) + 0.1)

def plot_sequence(plt, xs, counter, messages):

    for i,x in enumerate(xs):
        plt.title(messages[i])
        plt.plot(x_vals, values[1], lw=2.5, color=colors[1])
        plt.plot( [x, x], [0,fs[1](x)/integrate.quad(fs[1], leftroot, rightroot)[0]], color = colors[3] )
        plt.savefig("%sannealing_plot_%d.png" %(plotdir, counter), bbox_inches="tight");
        plt.plot( [x, x], [0,fs[1](x)/integrate.quad(fs[1], leftroot, rightroot)[0]], color = colors[1] )
        counter += 1

    return counter

messages = ["Start feasible", "Always accept better proposals", "Accept wors proposals with probability", "Terminate if good enough"]
counter = plot_sequence(plt, [-2, -3, 1.3, 3.5], counter, messages)


annealing_data_1 = csvtools.read_csv("%sannealing_1.csv" %datadir, "x", "y")
print annealing_data_1["x"]

# matplotlib's title() call centers the title on the plot, but not the graph,
# so I used the text() call to customize where the title goes.
 
# Make the title big enough so it spans the entire plot, but don't make it
# so big that it requires two lines to show.
 
# Note that if the title is descriptive enough, it is unnecessary to include
# axis labels; they are self-evident, in this plot's case.
#plt.text(x_min + 1, y_min + 1, "Percentage of Bachelor's degrees conferred to women in the U.S.A."
       #", by major (1970-2012)", fontsize=17, ha="center")
 
# Always include your data source(s) and copyright notice! And for your
# data sources, tell your viewers exactly where the data came from,
# preferably with a direct link to the data. Just telling your viewers
# that you used data from the "U.S. Census Bureau" is completely useless:
# the U.S. Census Bureau provides all kinds of data, so how are your
# viewers supposed to know which data set you used?
#plt.text(x_min + 3, -8, "Data source: nces.ed.gov/programs/digest/2013menu_tables.asp"
       #"\nAuthor: Randy Olson (randalolson.com / @randal_olson)"
       #"\nNote: Some majors are missing because the historical data "
       #"is not available for them", fontsize=10)
 
# Finally, save the figure as a PNG.
# You can also save it as a PDF, JPEG, etc.
# Just change the file extension in this call.
# bbox_inches="tight" removes all the extra whitespace on the edges of your plot.
plt.savefig("%sannealing_plot_%d.png" %(plotdir, counter), bbox_inches="tight");