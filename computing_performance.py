
from algorithm.util import *

if __name__ == '__main__':
    topo = 'topo1'
    al_lst = ['EAG-MOEAD', 'NSABC', 'MOEAD', 'MOEAD-OBL', 'MOEAD-SFLA', 'NSGA-II']

    for al in al_lst[:1]:
        METRIC, GD, IGD, HV = cal_metric(topo=topo, runtime=20, algorithm=al)
        write_metric(topo=topo, algorithm=al, runtime=20, metric=METRIC)

