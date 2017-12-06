from algorithm.operator import object_shell_sort
from algorithm.parameter import PROJECT_PATH as PATH

import json
import math
import random
import os
import matplotlib.pyplot as plt

'''
"S-shaped versus V-shaped transfer functions for binary Particle Swarm Optimization".
Swarm and Evolutionary Computation 9(2013) 1-14.
Seyedali Mirjalili.
'''
def func_trans_S1(x):
    return 1 / (1 + math.exp(-2 * x))

def func_trans_S2(x):
    return 1 / (1 + math.exp(-x))

def func_trans_S3(x):
    return 1 / (1 + math.exp(-x / 2))

def func_trans_S4(x):
    return 1 / (1 + math.exp(-x / 3))

def func_trans_V1(x):
    return abs(math.erf(math.sqrt(math.pi) * x / 2))

def func_trans_V2(x):
    return abs(math.tanh(x))

def func_trans_V3(x):
    return abs(x / math.sqrt(1 + x * x))

def func_trans_V4(x):
    return abs(2 * math.atan(math.pi * x / 2) / math.pi)

def func_levy(d):
    beta = float(3 / 2)
    pi = math.pi

    theta = (math.gamma(1 + beta) * math.sin(pi * beta / 2) / (math.gamma((1 + beta) / 2) * beta * math.pow(2, ((beta - 1) / 2))))
    sigma = math.pow(theta, (1 / beta))

    r1 = random.random()
    r2 = random.random()

    return 0.01 * r1 * sigma / math.pow(r2, (1 / beta))

def read_json_as_list(topo, algorithm):
    path = PATH + '\\solution\\' + topo + '\\PF-' + algorithm + '.json'
    list_ = []
    with open(path, 'r') as f:
        conf = json.load(f)
        for item in conf:
            list_.append(item)
        f.close()
    
    return list_

def write_list_to_json(topo, algorithm, solutions):
    path = PATH + '\\solution\\' + topo + '\\PF-' + algorithm + '.json'
    solution = []
    for sol in solutions:
        solution.append(sol.to_dict())
    
    object_shell_sort(solution, 'loss')
    obj = solution[0]['delay']
    for item in solution[:]:
        if item['delay'] >= obj:
            solution.remove(item)
        else:
            obj = item['delay']
    
    with open(path, 'wb') as f:
        f.write(json.dumps(solution, indent=4))
        f.close()
        
def write_performance(property, topo, algorithm, lst):
    path = PATH + '\\solution\\' + topo + '\\' + property + '-' + algorithm + '.json'
    with open(path, 'wb') as f:
        f.write(json.dumps(lst, indent=4))
        f.close()

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
        temp = os.getcwd() + '\\solution\\' + topo + '\\PF-' + type + '.json'
        plot_pf(temp, type, color,describe)
    plt.show()
    
if __name__ == '__main__':
    pass
