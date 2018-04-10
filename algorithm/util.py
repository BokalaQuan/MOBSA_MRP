from algorithm.parameter import INF

import json
import math
import random
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import ttest_ind

FORMAT = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(format = FORMAT)
logger.setLevel(level='INFO')

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


def func_levy(d, beta):
    # beta = float(3 / 2)

    pi = math.pi

    theta = (np.math.gamma(1 + beta) * np.math.sin(pi * beta / 2) /
             (np.math.gamma((1 + beta) / 2) * beta * np.math.pow(2, ((beta - 1) / 2))))
    sigma = np.math.pow(theta, (1 / beta))

    u = np.random.randn(d) * sigma
    v = np.random.randn(d)

    step = u / (abs(v) ** (1 / beta))

    return 0.01 * step




'''
Multi-objective Optimization Algorithms' Performance Indicators.

Convergence Metrics: GD, Epsilon
Diversity Metrics: Spread, OS
Complex: IGD, HV

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

def cal_Epsilon(pIdeal, pReal):
    solution = []

    for rel in pReal:
        I = []
        for ide in pIdeal:
            I.append(max(rel['fit'][0]/ide['fit'][0], rel['fit'][1]/ide['fit'][1]))

        solution.append(np.min(I))

    return np.max(solution)


def cal_Spread(pIdeal, pReal):
    len_Real = len(pReal)
    len_Ideal = len(pIdeal)

    df = np.linalg.norm(np.array(pIdeal[0]['fit']) - np.array(pReal[0]['fit']))
    dl = np.linalg.norm(np.array(pIdeal[len_Ideal-1]['fit']) - np.array(pReal[len_Real-1]['fit']))

    d_lst = []
    for index in range(len_Real-1):
        d_lst.append(np.linalg.norm(np.array(pReal[index]['fit']) -
                                    np.array(pReal[index+1]['fit'])))

    D_lst = np.array(d_lst)
    mean = D_lst.mean()
    tmp = abs(D_lst - mean)

    return (df + dl + tmp.sum()) / (df + dl + (len_Real-1) * mean)


def cal_OS(pIdeal, pReal):
    rel_top = pReal[0]['fit']
    rel_low = pReal[len(pReal)-1]['fit']

    ide_top = pIdeal[0]['fit']
    ide_low = pIdeal[len(pIdeal)-1]['fit']

    return (abs(rel_low[0]-rel_top[0])*abs(rel_low[1]-rel_top[1])) \
           / (abs(ide_low[0]-ide_top[0])*abs(ide_low[1]-ide_top[1]))


def cal_metric(topo=None, runtime=None, algorithm=None):
    pf_ideal = read_json_as_list(topo=topo, algorithm='IDEAL')
    p0 = pf_ideal[0]['fit']
    p1 = pf_ideal[len(pf_ideal) - 1]['fit']
    ref = [p0[0] + 0.1 * abs(p0[0] - p1[0]),
           p1[1] + 0.1 * abs(p0[1] - p1[1])]

    GD = []
    IGD = []
    HV = []
    Epsilon = []
    Spread = []


    pf_lst = []
    for i in range(runtime):
        pf = read_json_as_list(topo=topo, algorithm=algorithm, runtime=i+1)
        pf_lst.append(pf)

    for pf in pf_lst:
        GD.append(cal_GD(pf_ideal, pf))
        IGD.append(cal_IGD(pf_ideal, pf))
        HV.append(cal_HV(pf, ref))
        Epsilon.append(cal_Epsilon(pf_ideal, pf))
        Spread.append(cal_Spread(pf_ideal, pf))

    GD = np.array(GD)
    IGD = np.array(IGD)
    HV = np.array(HV)
    Epsilon = np.array(Epsilon)
    Spread = np.array(Spread)

    mean_GD = '%.2f' % GD.mean()
    mean_IGD = '%.2f' % IGD.mean()
    mean_HV = '%.2f' % HV.mean()
    mean_E = '%.2f' % Epsilon.mean()
    mean_S = '%.2f' % Spread.mean()

    std_GD = '%.2f' % GD.std()
    std_IGD = '%.2f' % IGD.std()
    std_HV = '%.2f' % HV.std()
    std_E = '%.2f' % Epsilon.std()
    std_S = '%.2f' % Spread.std()


    GD_ = {'Mean': mean_GD,
           'Std': std_GD}

    IGD_ = {'Mean': mean_IGD,
           'Std': std_IGD}

    HV_ = {'Mean': mean_HV,
           'Std': std_HV}

    Epsilon_ = {'Mean': mean_E,
           'Std': std_E}

    Spread_ = {'Mean': mean_S,
           'Std': std_S}


    METRIC = {'GD': GD_,
              'IGD': IGD_,
              'HV': HV_,
              'Epsilon': Epsilon_,
              'Spread': Spread_,
              'GD_lst': list(GD),
              'IGD_lst': list(IGD),
              'HV_lst': list(HV),
              'Epsilon_lst': list(Epsilon),
              'Spread_': list(Spread)}

    return METRIC


def read_metric(topo=None, algorithm=None):
    path = os.getcwd() + '/solution/' + topo + '/Metric-' + algorithm + '.json'

    with open(path, 'r') as f:
        conf = json.load(f)
        GD = conf['GD_lst']
        IGD = conf['IGD_lst']
        HV = conf['HV_lst']
        Epsilon = conf['Epsilon_lst']
        Spread = conf['Spread_']


    return GD, IGD, HV, Epsilon, Spread


def write_metric(topo=None, algorithm=None, metric=None):
    path = os.getcwd() + '/solution/' + topo + '/Metric-' + algorithm + '.json'

    with open(path, 'w+') as f:
        f.write(json.dumps(metric, indent=4))


def read_json_as_list(topo, algorithm, runtime=None):
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
            logger.info('%s is not found', path)

    else:
        path = os.getcwd() + '/solution/' + topo + '/PF-' + algorithm + \
               '-' + str(runtime) + '.json'
        try:
            with open(path, 'r') as f:
                conf = json.load(f)
                for item in conf:
                    list_.append(item)
            # logger.info('Read solutions successful.')
        except IOError:
            logger.info('%s is not found', path)

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
            if type(sol) is dict:
                solution.append(sol)
            else:
                solution.append(sol.to_dict())

    solution.sort(key=lambda x:x['fit'][1], reverse=False)

    obj_1 = solution[0]['fit'][0]
    obj_2 = solution[0]['fit'][1]

    for item in solution[1:]:
        if item['fit'][0] > obj_1:
            solution.remove(item)
        elif item['fit'][0] == obj_1 and item['fit'][1] == obj_2:
            solution.remove(item)
        else:
            obj_1 = item['fit'][0]
            obj_2 = item['fit'][1]

    try:
        with open(path, 'w+') as f:
            f.write(json.dumps(solution, indent=4))
        # logger.info('Write solutions successful.')

    except Exception:
        logger.info('%s is not found', path)
        pass


def update_ideal_pf(topo, algorithms):
    union_pf = []
    for al in algorithms:
        union_pf.extend(read_json_as_list(topo=topo, algorithm=al))

    union_pf.extend(read_json_as_list(topo=topo, algorithm='IDEAL'))

    write_list_to_json(topo=topo, algorithm='IDEAL', solutions=union_pf)




def func(topo=None, algorithm=None, runtime=None):
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
        tmp = os.getcwd() + '/solution/' + topo + '/PF-' + \
              algorithm + '-' + str(runtime) + '.json'

        x = []
        y = []

        with open(tmp, 'r') as f:
            conf = json.load(f)
            for item in conf:
                x.append(item['fit'][0])
                y.append(item['fit'][1])
        f.close()
        data = [x, y]

    return data


def plot_ps_by_different_algorithm(topo=None, algorithms=None, runtime=None, show=False,
                                   title=None):
    labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

    plt.figure()
    for item in algorithms:
        data = func(topo=topo, algorithm=item, runtime=runtime)
        plt.scatter(data[0], data[1], alpha=0.4)

    # plt.xlabel('Average End-to-End Delay (ms)', fontsize=12)
    plt.xlabel('Average End-to-End Delay (ms)')
    # plt.ylabel('Average Package Loss Rate (%)', fontsize=12)
    plt.ylabel('Average Package Loss Rate (%)')
    # plt.legend(algorithms, fontsize=10)
    plt.legend(labels)
    # plt.title(topo.title(), fontsize=10)
    plt.title(title)
    fig_path = os.getcwd()+'/solution/'+topo+'/'+topo.title()+'_PF.png'
    plt.savefig(fig_path, dpi=600)

    if show:
        plt.show()
    else:
        pass


def plot_performance_as_boxplot(topo=None, metric=None, algorithms=None, lst=None, show=False):
    plt.figure()
    plt.boxplot(lst, labels=algorithms)
    plt.xticks()
    plt.yticks()
    plt.xlabel('Algorithms')
    plt.ylabel(metric+'-Metric values')
    plt.title(topo.title())
    fig_path = os.getcwd()+'/solution/'+topo+'/'+topo.title()+'_'+metric+'_Metric.png'
    plt.savefig(fig_path, dpi=600)

    if show:
        plt.show()
    else:
        pass


def boxplot(filename=None, lst=None, titles=None, labels=None):
    # labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

    plt.figure(dpi=600)
    fig, axes = plt.subplots(2, 2)
    ax1 = axes[0, 0]
    ax2 = axes[0, 1]
    ax3 = axes[1, 0]
    ax4 = axes[1, 1]
    #
    ax1.boxplot(lst[0], labels=labels)
    ax2.boxplot(lst[1], labels=labels)
    ax3.boxplot(lst[2], labels=labels)
    ax4.boxplot(lst[3], labels=labels)

    ax1.set_title(titles[0])
    ax2.set_title(titles[1])
    ax3.set_title(titles[2])
    ax4.set_title(titles[3])


    # plt.show()

    plt.tight_layout(pad=1.0)

    fig_path = os.getcwd()+'/solution/'+filename.title()+'_Metric.png'
    plt.savefig(fig_path, dpi=600)
    #
