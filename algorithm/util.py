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
            fit_pi = np.array(pi['fit'])
            temp_ = np.linalg.norm(fit_pi - fit_pr)
            temp = temp_ if temp_ < temp else temp
        vol += temp ** 2

    return math.sqrt(vol) / len(pReal)

def cal_HV(pReal, ref):
    '''
    Hyper-volume.
    '''
    # hv = (ref[0] - pReal[0]['fit'][0]) * (ref[1] - pReal[0]['fit'][1])
    # for i in range(1, len(pReal)):
    #     hv += (pReal[i - 1]['fit'][0] - pReal[i]['fit'][0]) * \
    #           (ref[1] - pReal[i]['fit'][1])
    hv = 0.0
    hv += (ref[1] - pReal[0]['fit'][1]) * (ref[0] - pReal[0]['fit'][0])
    for i in range(1, len(pReal)):
        hv += (ref[1] - pReal[i]['fit'][1]) * \
              (pReal[i-1]['fit'][0] - pReal[i]['fit'][0])

    return hv

def cal_C(p_lst1, p_lst2):
    '''
    C-Metric
    :param p_lst1:
    :param p_lst2:
    :return:
    '''
    lst = set()
    for ind2 in p_lst2:
        for ind1 in p_lst1:
            if ind1['fit'][0] < ind2['fit'][0] and ind1['fit'][1] < ind2['fit'][1]:
                lst.add(ind2)

    return float(len(lst)) / len(p_lst2)

def cal_metric(topo=None, runtime=None, algorithm=None):
    pf_ideal = read_json_as_list(topo=topo, algorithm='IDEAL')
    p0 = pf_ideal[0]['fit']
    p1 = pf_ideal[len(pf_ideal) - 1]['fit']
    ref = [p0[0] + 0.1 * abs(p0[0] - p1[0]),
           p1[1] + 0.1 * abs(p0[1] - p1[1])]

    GD = []
    IGD = []
    HV = []
    pf_lst = []
    for i in range(runtime):
        pf = read_json_as_list(topo=topo, algorithm=algorithm, runtime=i+1)
        pf_lst.append(pf)

    for pf in pf_lst:
        GD.append(cal_GD(pf_ideal, pf))
        IGD.append(cal_IGD(pf_ideal, pf))
        HV.append(cal_HV(pf, ref))

    GD = np.array(GD)
    IGD = np.array(IGD)
    HV = np.array(HV)

    min_GD = '%.4f' % GD.min()
    min_IGD = '%.4f' % IGD.min()
    min_HV = '%.4f' % HV.min()

    max_GD = '%.4f' % GD.max()
    max_IGD = '%.4f' % IGD.max()
    max_HV = '%.4f' % HV.max()

    mean_GD = '%.4f' % GD.mean()
    mean_IGD = '%.4f' % IGD.mean()
    mean_HV = '%.4f' % HV.mean()

    std_GD = '%.4f' % GD.std()
    std_IGD = '%.4f' % IGD.std()
    std_HV = '%.4f' % HV.std()

    GD_ = {'Max': max_GD,
           'Min': min_GD,
           'Mean': mean_GD,
           'Std': std_GD}

    IGD_ = {'Max': max_IGD,
           'Min': min_IGD,
           'Mean': mean_IGD,
           'Std': std_IGD}

    HV_ = {'Max': max_HV,
           'Min': min_HV,
           'Mean': mean_HV,
           'Std': std_HV}

    METRIC = {'GD': GD_,
              'IGD': IGD_,
              'HV': HV_}

    return METRIC, GD, IGD, HV

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
        path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + \
               '-' + str(runtime) + '.json'
        try:
            with open(path, 'r') as f:
                conf = json.load(f)
                for item in conf:
                    list_.append(item)
            f.close()
        except IOError:
            print path, 'not found!'

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
            if type(sol) is dict:
                solution.append(sol)
            else:
                solution.append(sol.to_dict())

    solution.sort(cmp=None, key=lambda x:x['fit'][1], reverse=False)

    obj_delay = solution[0]['fit'][0]
    obj_loss = solution[0]['fit'][1]
    for item in solution[:]:
        if item['fit'][0] > obj_delay:
            solution.remove(item)
        elif item['fit'][0] == obj_delay and item['fit'][1] == obj_loss:
            solution.remove(item)
        else:
            obj_delay = item['fit'][0]
            obj_loss = item['fit'][1]

    with open(path, 'wb') as f:
        f.write(json.dumps(solution, indent=4))
        f.close()

def update_ideal_pf(topo, algorithms):
    union_pf = []
    for al in algorithms:
        union_pf.extend(read_json_as_list(topo=topo, algorithm=al))

    union_pf.extend(read_json_as_list(topo=topo, algorithm='IDEAL'))

    write_list_to_json(topo=topo, algorithm='IDEAL', solutions=union_pf)

def read_metric_as_json(runtime=None, metric=None):
    tmp = {'Runtime': runtime,
           'Metric': metric}

    return tmp

def write_metric(topo=None, algorithm=None, runtime=None, metric=None):
    if runtime is None:
        pass
    else:
        path = os.getcwd() + '/solution/' + topo + '/Metric-' + algorithm +  '.json'

        tmp = []
        for i in range(runtime):
            tmp.append(read_metric_as_json(runtime=i+1, metric=metric))

        with open(path, 'wb') as f:
            f.write(json.dumps(tmp, indent=4))

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

def plot_ps_by_different_algorithm(topo=None, algorithms=None):
    plt.figure()
    for item in algorithms:
        data = func(topo=topo, algorithm=item)
        plt.scatter(data[0], data[1], alpha=0.4)

    plt.xlabel('Arg_Delay (ms)', fontsize=12)
    plt.ylabel('Arg_PLR (%)', fontsize=12)
    plt.legend(algorithms, fontsize=10)
    plt.savefig(topo.title()+"_PF.png", dpi=900)

def plot_performance_as_boxplot(topo=None, metric=None, algorithms=None, lst=None):
    plt.figure()
    plt.boxplot(lst, labels=algorithms)
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    plt.xlabel('Algorithms', fontsize=10)
    plt.ylabel(metric+'-Metric values', fontsize=10)
    plt.title(topo.title(), fontsize=10)
    plt.savefig(topo.title() + '_' + metric + '_Metric.png', dpi=900)