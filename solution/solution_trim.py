from algorithm.operator import object_shell_sort
from algorithm.util import read_json_as_list

import json
import os

def trim_solution(topo, algorithms):
    path = os.getcwd() + '\\' + topo + '\\PF-IDEAL'  + '.json'
    solutions = []
    for al in algorithms:
        solutions.extend(read_json_as_list(topo, al))
    
    object_shell_sort(solutions, 'loss')
    
    obj = solutions[0]['delay']
    for item in solutions[:]:
        if item['delay'] >= obj:
            solutions.remove(item)
        else:
            obj = item['delay']
            
    with open(path, 'wb') as f:
        f.write(json.dumps(solutions, indent=4))
        f.close()
        
if __name__ == '__main__':
    trim_solution('topo6')
    