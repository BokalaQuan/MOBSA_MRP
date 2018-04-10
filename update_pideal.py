import sys

from algorithm.util import *

"""
Topology list:

--------------------------------------------
| Rand_Topo | SNDlib_Topo | Zoo_Topo       |
--------------------------------------------
| Rand1     | germany50   | AttpMpls       |
| Rand2     | india35     | BtNorthAmerica |
| Rand3     | ta1         | HiberniaGlobal |
| Rand4     | ta2         | Tinet          |
| Rand5     |-------------------------------
| Rand6     |
| Rand7     |
| Rand8     |
-------------

Algorithms list:

----------------------------------------------------
| NSGA-II | MOEA/D | SPEA2 | MOPSO | PBIL1 | PBIL2 |
|NSABC | EAG-MOEAD | NSACO | Jaya |
----------------------------------------------------

"""

PATHs = {'Rand': '/Rand_Topo/',
         'SNDlib': '/SNDlib_Topo/',
         'Zoo': '/Zoo_Topo/'}

if __name__ == '__main__':

    # topo_lst = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topo_lst = ['germany50', 'india35', 'ta1', 'ta2']
    topo_lst = ['AttMpls', 'BtNorthAmerica', 'HiberniaGlobal', 'Tinet']

    alst = ['NSABC', 'MOEA-PCGG', 'SPEA2', 'MOEAD',
            'EAG-MOEAD', 'MOPSO', 'MOSFLA', 'PBIL']

    runtime = 20
    # runtime = 10

    for topo in topo_lst[:]:
        for al in alst[:]:
            lst = []
            for i in range(runtime):
                lst.extend(read_json_as_list(topo=topo, algorithm=al, runtime=i+1))

            write_list_to_json(topo=topo, algorithm=al, solutions=lst)
        update_ideal_pf(topo=topo, algorithms=alst)