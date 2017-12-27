from algorithm.parameter import INF

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

    theta = (math.gamma(1 + beta) * math.sin(pi * beta / 2) /
             (math.gamma((1 + beta) / 2) * beta * math.pow(2, ((beta - 1) / 2))))
    sigma = math.pow(theta, (1 / beta))

    r1 = random.random()
    r2 = random.random()

    return 0.01 * r1 * sigma / math.pow(r2, (1 / beta))

'''
Multi-objective Optimization Algorithms' Performance Indicators 
'''
def cal_IGD(pIdeal, pReal):
    '''
    Inverted Generational Distance
    '''
    vol = 0.0
    for pi in pIdeal:
        temp = INF
        fit_pi = np.array(pi['fit'])
        for pr in pReal:
            fit_pr = np.array(pr['fit'])

            temp_ = np.linalg.norm(fit_pi - fit_pr)
            temp = temp_ if temp_ < temp else temp
        vol += temp

    return vol / len(pIdeal)

def cal_GD(pIdeal, pReal):
    '''
    Generational Distance
    '''
    vol = 0.0
    for pr in pReal:
        temp = INF
        fit_pr = np.array(pr['fit'])
        for pi in pIdeal:
            # f1 = pr['delay'] - pi['delay']
            # f2 = pr['loss'] - pi['loss']
            fit_pi = np.array(pi['fit'])

            # temp_ = math.sqrt(f1 ** 2 + f2 ** 2)
            temp_ = np.linalg.norm(fit_pi - fit_pr)
            temp = temp_ if temp_ < temp else temp
        vol += temp ** 2

    return math.sqrt(vol) / len(pReal)

def cal_HV(pReal, ref):
    '''
    Hyper-volume.
    '''
    # hv = (ref[0] - pReal[0]['delay']) * (ref[1] - pReal[0]['loss'])
    hv = (ref[0] - pReal[0]['fit'][0]) * (ref[1] - pReal[0]['fit'][1])
    for i in range(1, len(pReal)):
        # hv += (pReal[i - 1]['delay'] - pReal[i]['delay']) * (ref[1] - pReal[i]['loss'])
        hv += (pReal[i - 1]['fit'][0] - pReal[i]['fit'][0]) * \
              (ref[1] - pReal[i]['fit'][1])

    return hv

def read_json_as_list(topo, algorithm, runtime=None):
    """

    :param topo:
    :param algorithm:
    :param runtime:
    :return:
    """
    list_ = []
    if runtime is None:
        path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + '.json'

        try:
            with open(path, 'r') as f:
                conf = json.load(f)
                for item in conf:
                    list_.append(item)
            f.close()
        except IOError:
            print path, 'not found!'

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
    """

    :param topo:
    :param algorithm:
    :param runtime:
    :param solutions:
    :return:
    """
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
            # solution.append(sol.to_dict())
            solution.append(sol)

    # solution.sort(cmp=None, key=lambda x:x['loss'], reverse=False)
    solution.sort(cmp=None, key=lambda x:x['fit'][1], reverse=False)

    # obj_delay = solution[0]['delay']
    obj_delay = solution[0]['fit'][0]
    # obj_loss = solution[0]['loss']
    obj_loss = solution[0]['fit'][1]
    for item in solution[:]:
        # if item['delay'] > obj_delay:
        if item['fit'][0] > obj_delay:
            solution.remove(item)
        # elif item['delay'] == obj_delay and item['loss'] == obj_loss:
        elif item['fit'][0] == obj_delay and item['fit'][1] == obj_loss:
            solution.remove(item)
        else:
            # obj_delay = item['delay']
            obj_delay = item['fit'][0]
            # obj_loss = item['loss']
            obj_loss = item['fit'][1]

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
            '-' + algorithm + '-' + str(runtime)  + '.json'
    with open(path, 'wb') as f:
        f.write(json.dumps(lst, indent=4))
        f.close()

def func(topo=None, algorithm=None, runtime=None):
    data = []

    if runtime is None:
        tmp = os.getcwd() + '/solution/' + topo + '/PF-' + \
            algorithm + '.json'

        x = []
        y = []

        with open(tmp, 'r') as f:
            conf = json.load(f)
            for item in conf:
                x.append(item['fit'][0])
                y.append(item['fit'][1])
        f.close()
        data = [x, y]
    else:
        for i in range(runtime):
            tmp = os.getcwd() + '/solution/' + topo + '/PF-' + \
                algorithm + '-' + str(i + 1) + '.json'

            x = []
            y = []

            with open(tmp, 'r') as f:
                conf = json.load(f)
                for item in conf:
                    x.append(item['fit'][0])
                    y.append(item['fit'][1])
            f.close()
            data.append([x, y])

    return data

def plot_ps_by_different_algorithm(topo=None, algorithms=None, title=None):
    plt.figure()
    for item in algorithms:
        data = func(topo=topo, algorithm=item)
        plt.scatter(data[0], data[1], alpha=0.5)


    plt.xlabel('Arg_plr (%)', fontsize=12)
    plt.ylabel('Arg_delay (ms)', fontsize=12)
    plt.legend(algorithms, fontsize=10)
    plt.savefig(title+".png", dpi=900)
    plt.show()

def plot_performance_as_boxplot():
    pass