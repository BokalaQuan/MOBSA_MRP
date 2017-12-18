from algorithm.util import *

import os

if __name__ == '__main__':
    
    topo = 'topo2'
    runtime = 5
    pf_list = []
    algorithms = ['NSGA-II', 'MOEAD', 'SPEA2']
    
    for al in algorithms:
        pf_list.append(read_json_as_list(topo=topo, algorithm=al, runtime=runtime))
        
    
        
    
    
    