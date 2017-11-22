from parameter import INF

import math

'''
Inverted Generational Distance
'''
def cal_IGD(pIdeal, pReal):
    vol = 0.0
    for pi in pIdeal:
        temp = INF
        for pr in pReal:
            f1 = pi['delay'] - pr['delay']
            f2 = pi['loss'] - pr['loss']
            temp_ = math.sqrt(f1 ** 2 + f2 ** 2)
            temp = temp_ if temp_ < temp else temp
        vol += temp
    
    return vol / len(pIdeal)
    

'''
Generational Distance
'''
def cal_GD(pIdeal, pReal):
    vol = 0.0
    for pr in pReal:
        temp = INF
        for pi in pIdeal:
            f1 = pr['delay'] - pi['delay']
            f2 = pr['loss'] - pi['loss']
            temp_ = math.sqrt(f1 ** 2 + f2 ** 2)
            temp = temp_ if temp_ < temp else temp
        vol += temp ** 2

    return math.sqrt(vol) / len(pReal)

'''
Hypervolume
'''
def cal_HV(pReal, ref):
    hv = (ref[0] - pReal[0]['delay']) * (ref[1] - pReal[0]['loss'])
    
    for i in range(1, len(pReal)):
        hv += (pReal[i-1]['delay'] - pReal[i]['delay']) * (ref[1] - pReal[i]['loss'])
        
    return hv


def cal_os():
    pass


    

