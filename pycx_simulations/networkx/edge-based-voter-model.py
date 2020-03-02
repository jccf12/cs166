import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd

def initialize():
    global g, t, timesteps, ones
    ones = 0
    t = -1
    timesteps = []
    g = nx.karate_club_graph()
    g.pos = nx.spring_layout(g)
    for i in g.nodes:
        g.nodes[i]['state'] = 1 if random() < .5 else 0
        ones += g.nodes[i]['state']
    print('Initializing with {} ones'.format(ones))

def observe():
    global g, t, timesteps, ones
    cla()
    ax1 = subplot(2,1,1)
    nx.draw(g, vmin = 0, vmax = 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos)
    if timesteps:
        ax2 = subplot(2,1,2)
        m = round(np.mean(timesteps),2)
        std = np.std(timesteps)
        cf = (round(m-1.96*std,2),round(m+1.96*std,2))
        ax2.scatter(list(range(len(timesteps))),timesteps, s=1, alpha = 0.5)
        ax2.plot(list(range(len(timesteps))),[m]*len(timesteps), color = "black")
        ax2.fill_between(list(range(len(timesteps))),[cf[0]]*len(timesteps),[cf[1]]*len(timesteps),alpha=0.2, color ="green")
        
        ax2.title.set_text('Timesteps to reach consensus (Edge-based Model)')
        ax2.set_ylabel('Timesteps')
        ax2.set_xlabel('Simulation no. \nMean = {}, Confidence Interval = {}'.format(m,cf))


def update():
    global g, t, timesteps, ones
    if t == -1:
        t = 0
        for _ in range(1000):
            homogeinity = False
            while not homogeinity:
                edge = rd.choice(list(g.edges))
                l = rd.randint(0,1)
                listener = edge[l]
                speaker = edge[1-l]
                ones+= g.nodes[speaker]['state'] - g.nodes[listener]['state']
                g.nodes[listener]['state'] = g.nodes[speaker]['state']
                current = -1
                past = -1
                t+=1
                if ones == len(g) or ones == 0:
                    homogeinity = True
                    timesteps.append(t)
                    t = 0
                    ones = 0
                    for i in g.nodes:
                        g.nodes[i]['state'] = 1 if random() < .5 else 0
                        ones += g.nodes[i]['state']
    else:
        edge = rd.choice(list(g.edges))
        l = rd.randint(0,1)
        listener = edge[l]
        speaker = edge[1-l]
        ones+= g.nodes[speaker]['state'] - g.nodes[listener]['state']
        g.nodes[listener]['state'] = g.nodes[speaker]['state']
        current = -1
        past = -1
        t+=1
        if ones == len(g) or ones == 0:
            timesteps.append(t)
            t = 0
            ones = 0
            for i in g.nodes:
                g.nodes[i]['state'] = 1 if random() < .5 else 0
                ones += g.nodes[i]['state']


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])