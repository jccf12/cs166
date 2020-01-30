import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import matplotlib.pyplot as plt

n = 100 # size of space: n x n
p = 0.4 # probability of initially panicky individuals

def initialize():
    global config, nextconfig, current_density
    current_density = []
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random() < p else 0
    nextconfig = zeros([n, n])

    
def observe():
    global config, nextconfig, current_density
    cla()
    subplots_adjust(bottom=0.3,top=0.70, wspace = 0.6)
    ax1 = plt.subplot(1,2,1)
    ax1.imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    ax2 = plt.subplot(1,2,2)
    ax2.plot(list(range(len(current_density))),current_density)


def update():
    global config, nextconfig, current_density
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx) % n, (y + dy) % n]
            if config[x,y] == 1:
                nextconfig[x, y] = 1 if (count == 2 or count == 3)  else 0
            else:
                nextconfig[x,y] = 1 if count == 3 else 0
    config, nextconfig = nextconfig, config
    current_density.append(sum(config)/(n**2))


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])