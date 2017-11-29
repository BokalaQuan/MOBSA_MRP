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
    plt.xlabel('Ave_plr (%)',fontsize=20)
    plt.ylabel('Ave_delay (ms)',fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    
    plt.plot(x, y, color)


def plot_ps(topo, types, colors, describe):
    for type, color in zip(types, colors):
        temp = os.getcwd() + '\\' + topo + '\\pf_' + type + '.json'
        plot_pf(temp, type, color, describe)
    plt.legend(types,fontsize=20)
    plt.title('Topo6: Node=150, Edge=352',fontsize=20)
    plt.show()
    

if __name__ == '__main__':
    path = os.getcwd() + '\\topo2\\pf_' + 'mobso' + '.json'
    path1 = os.getcwd() + '\\topo2\\pf_' + 'ideal' + '.json'
    
    plot_ps('topo6', ['ideal', 'mobso', 'mopso'], ['ko', 'r*', 'b^'], describe=None)
