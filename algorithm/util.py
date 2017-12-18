from algorithm.operator import object_shell_sort

import json
import math
import random
import os
import numpy as np
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


def read_json_as_list(topo, algorithm, runtime=None):
    list_ = []
    if runtime is None:
        path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + '.json'

        with open(path, 'r') as f:
            conf = json.load(f)
            for item in conf:
                list_.append(item)
        f.close()
    else:
        for i in range(runtime):
            path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + \
                '-' +str(runtime)  + '.json'
            tmp = []
            with open(path, 'r') as f:
                conf = json.load(f)
                for item in conf:
                    tmp.append(item)
            f.close()
            list_.extend(tmp)

    return list_

def write_list_to_json(topo=None, algorithm=None, runtime=None, solutions=None):
    if runtime is None:
        path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + '.json'
    else:
        path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + \
            '-' +str(runtime)  + '.json'
    
    solution = []
    if algorithm == 'IDEAL':
        solution = solutions
    else:
        for sol in solutions:
            solution.append(sol.to_dict())

    object_shell_sort(solution, 'loss')
    
    obj_delay = solution[0]['delay']
    obj_loss = solution[0]['loss']
    for item in solution[:]:
        if item['delay'] > obj_delay:
            solution.remove(item)
        elif item['delay'] == obj_delay and item['loss'] == obj_loss:
            solution.remove(item)
        else:
            obj_delay = item['delay']
            obj_loss = item['loss']

    with open(path, 'wb') as f:
        f.write(json.dumps(solution, indent=4))
        f.close()

def update_ideal_pf(topo, algorithms, runtime=None):
    union_pf = []
    for al in algorithms:
        if runtime is None:
            union_pf.extend(read_json_as_list(topo=topo, algorithm=al))
        else:
            union_pf.extend(read_json_as_list(topo=topo, algorithm=al, runtime=runtime))
    
    union_pf.extend(read_json_as_list(topo=topo, algorithm='IDEAL'))
    
    write_list_to_json(topo=topo, algorithm='IDEAL', solutions=union_pf)
    
    
def write_performance(property=None, topo=None, algorithm=None, runtime=None, lst=None):
    path = os.getcwd() + '/solution/' + topo + '/' + property + \
            '-' + algorithm + str(runtime)  + '.json'
    with open(path, 'wb') as f:
        f.write(json.dumps(lst, indent=4))
        f.close()

def func(topo=None, algorithm=None, runtime=None):
    x = []
    y = []
    data = []

    if runtime is None:
        tmp = os.getcwd() + '/solution/' + topo + '/PF-' + \
            algorithm + '.json'

        with open(tmp, 'r') as f:
            conf = json.load(f)
            for item in conf:
                x.append(item['loss'])
                y.append(item['delay'])
        f.close()
        data = [x, y]
    else:
        for i in range(runtime):
            tmp = os.getcwd() + '/solution/' + topo + '/PF-' + \
                algorithm + '-' + str(i + 1) + '.json'

            with open(tmp, 'r') as f:
                conf = json.load(f)
                for item in conf:
                    x.append(item['loss'])
                    y.append(item['delay'])
            f.close()
            data.append([x, y])

    return data

def plot_ps_by_same_algorithm(topo=None, algorithm=None, runtime=None):
    with plt.style.context('Solarize_Light2'):
        data = func(topo=topo, algorithm=algorithm, runtime=runtime)
        for i in range(runtime):
            plt.plot(data[i][0], data[i][1])

        plt.title(algorithm)
        plt.xlabel('Ave_plr (%)', fontsize=14)
        plt.ylabel('Ave_delay (ms)', fontsize=14)

    plt.show()


def plot_ps_by_different_algorithm(topo=None, algorithms=None):
    styles = ['r^', 'ko']
    for item, sty in zip(algorithms, styles):
        data = func(topo=topo, algorithm=item)
        plt.plot(data[0], data[1], sty)

    plt.xlabel('Ave_plr (%)', fontsize=14)
    plt.ylabel('Ave_delay (ms)', fontsize=14)
    plt.legend(algorithms)
    plt.show()





if __name__ == '__main__':
    x = np.linspace(-10, 10, 1000)
    y = np.array([func_trans_V4(i) for i in x])
    
    plt.plot(x, y)
    plt.show()
