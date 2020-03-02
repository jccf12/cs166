# Simple CA simulator in Python
#
# *** Forest fire ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

# Modified to run with Python 3

import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP
from matplotlib.colors import LinearSegmentedColormap

cMap = []
for value, colour in zip([0,0.33,0.66,1],["lightgray", "Green", "Red", "Black"]):
    cMap.append((value, colour))

customColourMap = LinearSegmentedColormap.from_list("custom", cMap)

RD.seed()

width = 100
height = 100
size = width*height
initProb = 0.7
i = 0.2 #ignition probability 
empty, tree, fire, char = range(4)

def init():
    global time, config, nextConfig, tree_proportion, burning_proportion, death_proportion, tree_count, burning_count, char_count, fire_stopped, intialp
    initialp = []
    fire_stopped = []
    tree_proportion = []
    burning_proportion = [] 
    death_proportion = []
    tree_count = -1
    burning_count = 1
    char_count = 0
    time = 0

    config = SP.zeros([height, width])
    for x in range(width):
        for y in range(height):
            if RD.random() < initProb:
                state = tree
                tree_count+=1
            else:
                state = empty
            config[y, x] = state
    config[height//2, width//2] = fire

    nextConfig = SP.zeros([height, width])

def draw():
    global time, tree_proportion, burning_proportion, death_proportion, tree_count, burning_count, char_count
    PL.cla()
    PL.subplots_adjust(hspace = 0.35)
    ax1 = PL.subplot(2,2,1)
    ax1.pcolor(config, vmin = 0, vmax = 3, cmap = customColourMap)
    ax1.axis('image')
    ax1.title.set_text('t = ' + str(time))

    if time > 0:
        burning = burning_proportion[-1]
        trees = tree_proportion[-1]
        deads = death_proportion[-1]
    else:
        burning = 0
        trees = tree_count/size
        deads = 0
    ax3 = PL.subplot(2,2,2)
    ax3.bar([1],[trees], label ="Alive Trees", color = "green")
    ax3.bar([1],[burning], bottom = [trees], label="Burning", color = "red")
    ax3.bar([1],[deads], bottom = [trees+burning], label="Char", color = "black")
    ax3.bar([1],[1-trees-deads-burning], bottom = [trees+burning+deads], label = "Empty cells", color ="lightgray")
    ax3.title.set_text('Distribution of the Forest')
    ax3.set_ylabel('Density')

    ax2 = PL.subplot(2,2,3)
    ax2.plot(list(range(time)),burning_proportion, label = "burning count = {}".format(burning_count), color = "red")
    ax2.plot(list(range(time)),tree_proportion, label = "tree count = {}".format(tree_count), color ="green")
    ax2.plot(list(range(time)),death_proportion, label = "char count = {}".format(char_count), color ="black")
    ax2.set_ylim([0,1])
    ax2.legend()
    ax2.set_xlabel('time')
    ax2.set_ylabel('Density')
    ax2.title.set_text('Ignition probability = {}'.format(i))


def step():
    global time, config, nextConfig, tree_count, burning_count, char_count, fire_stopped, intialp

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == fire:
                state = char
            elif state == tree:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == fire:
                            if RD.random() < i:
                                state = fire
            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config
    tree_count = SP.count_nonzero(config == 1)
    burning_count = SP.count_nonzero(config == 2)
    if burning_count == 0:
        fire_stopped.append(time) 
        intialp.append(initProb)
    char_count = SP.count_nonzero(config == 3)
    tree_proportion.append(tree_count/size)
    burning_proportion.append(burning_count/size)
    death_proportion.append(char_count/size)


import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])