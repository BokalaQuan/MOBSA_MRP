from algorithm.operator import object_shell_sort

import json
import os

def read_solution(path):
    sols = []
    with open(path, 'r') as f:
        conf = json.load(f)
        for item in conf:
            sols.append(item)
        f.close()
    return sols
    
def trim_solution(topo):
    PATH1 = os.getcwd() + '\\' + topo + '\\pf_' + 'nsga2' + '.json'
    PATH2 = os.getcwd() + '\\' + topo + '\\pf_' + 'mobas' + '.json'
    PATH3 = os.getcwd() + '\\' + topo + '\\pf_' + 'mopso' + '.json'
    PATH4 = os.getcwd() + '\\' + topo + '\\pf_ideal.json'
    
    solutions = []
    solutions.extend(read_solution(PATH1))
    solutions.extend(read_solution(PATH2))
    solutions.extend(read_solution(PATH3))
    solutions.extend(read_solution(PATH4))
    
    object_shell_sort(solutions, 'loss')
    
    obj = solutions[0]['delay']
    for item in solutions[:]:
        if item['delay'] >= obj:
            solutions.remove(item)
        else:
            obj = item['delay']
            
    with open(PATH4, 'w') as f:
        f.write(json.dumps(solutions, indent=4))
        f.close()
        
if __name__ == '__main__':
    trim_solution('topo6')
    