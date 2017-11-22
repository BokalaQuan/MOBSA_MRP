import json
import os
import matplotlib.pyplot as plt


def plot_pf(filename, type, color, describe):
    x = []
    y = []
    with open(filename, 'r') as f:
        conf = json.load(f)
        for item in conf:
            x.append(item['loss'])
            y.append(item['delay'])
        f.close()
    plt.xlabel('Ave_plr (%)')
    plt.ylabel('Ave_delay (ms)')
    plt.legend(describe, numpoints=2)
    plt.plot(x, y, color)


def plot_ps(topo, types, colors, describe):
    for type, color in zip(types, colors):
        temp = os.getcwd() + '\\solution\\' + topo + '\\pf_' + type + '.json'
        plot_pf(temp, type, color, describe)
    plt.show()
    

if __name__ == '__main__':
    pass
