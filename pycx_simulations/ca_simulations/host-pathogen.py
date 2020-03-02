# Simple CA simulator in Python
#
# *** Hosts & Pathogens ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

# Modified to run with Python 3

import matplotlib
import pandas as pd
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP

RD.seed()

width = 50
height = 50
size = width*height
initProb = 0.01
infectionRate = 0.85
regrowthRate = 0.15

def init():
    global time, config, nextConfig, infected_proportion, healthy_proportion

    healthy_proportion = []
    infected_proportion = []
    time = 0
    
    config = SP.zeros([height, width])
    for x in range(width):
        for y in range(height):
            if RD.random() < initProb:
                state = 2
            else:
                state = 1
            config[y, x] = state

    nextConfig = SP.zeros([height, width])

def draw():
    global infected_proportion, time, healthy_proportion
    PL.cla()
    PL.subplots_adjust(bottom=0.1,top=0.9, wspace = 0.6)
    ax1 = PL.subplot(2,2,1)
    ax1.pcolor(config, vmin = 0, vmax = 2, cmap = PL.cm.jet)
    ax1.axis('image')
    ax1.title.set_text('t = ' + str(time))

    if time > 0:
        infected = infected_proportion[-1]
        healthy = healthy_proportion[-1]
    else:
        infected = 0
        healthy = 0
    ax3 = PL.subplot(2,2,2)
    ax3.bar([1],[healthy], label ="Healthy", color = "#86f77c")
    ax3.bar([1],[infected], bottom = [healthy], label="Infected", color = "#850000")
    ax3.bar([1],[1-healthy-infected], bottom = [healthy+infected], label = "Unpopulated", color ="#0d0d85")
    ax3.title.set_text('Distribution of the population')
    ax3.set_ylabel('Proportion of the population')

    ax2 = PL.subplot(2,1,2)
    ax2.plot(list(range(time)),infected_proportion, label = "infected", color = "#850000")
    ax2.plot(list(range(time)),healthy_proportion, label = "healthy", color ="#86f77c")
    ax2.legend()
    ax2.set_xlabel('time')
    ax2.set_ylabel('Proportion of the population')

def step():
    global time, config, nextConfig

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 1:
                            if RD.random() < regrowthRate:
                                state = 1
            elif state == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 2:
                            if RD.random() < infectionRate:
                                state = 2
            else:
                state = 0

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config
    infected_proportion.append(SP.count_nonzero(config == 2)/size)
    healthy_proportion.append(SP.count_nonzero(config == 1)/size)

import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])