import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import math

n = 30 # number of nodes
k = 4 # number of neighbors of each node

def initialize():
    global g
    g = nx.Graph()
    #grid is 5x6
    I = int(n**(1/2))
    J = math.ceil(n/I)
    for i in range(I):
        for j in range(J):
            num = i*J+j+1
            if i>0:
                north = (i-1)*J+j+1
                g.add_edge(num,north)
            if j>0:
                west = i*J+j
                g.add_edge(num,west)
            if i<I-1:
                south = (i+1)*J+j+1
                g.add_edge(num,south)
            if j<J-1:
                east = i*J+j+2
                g.add_edge(num,east)
    g.pos = nx.spring_layout(g)
    g.count = 0

def observe():
    global g
    cla()
    nx.draw(g, pos = g.pos)

def update():
    global g
    g.count += 1
    if g.count % 20 == 0: # rewiring once in every 20 steps
        nds = list(g.nodes)
        i = rd.choice(nds)
        if g.degree[i] > 0:
            g.remove_edge(i, rd.choice(list(g.neighbors(i))))
            nds.remove(i)
            for j in g.neighbors(i):
                nds.remove(j)
            g.add_edge(i, rd.choice(nds))

    # simulation of node movement
    g.pos = nx.spring_layout(g, pos = g.pos, iterations = 5)

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])