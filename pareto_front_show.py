from algorithm.util import *

"""
Topology list:

--------------------------------------------
| Rand_Topo | SNDlib_Topo | Zoo_Topo       |
--------------------------------------------
| Rand1     | germany50   | AttpMpls       |
| Rand2     | india35     | BtNorthAmerica |
| Rand3     | ta1         | Chinanet |
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
# topo = 'Rand4'


if __name__ == '__main__':
    # topo_lst = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topo_lst = ['germany50', 'india35', 'ta1', 'ta2']
    topo_lst = ['AttMpls', 'BtNorthAmerica', 'Chinanet', 'Tinet']

    alst = ['NSABC', 'MOEA-PCGG', 'SPEA2', 'MOEAD', 'EAG-MOEAD', 'MOSFLA']

    # tlst = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']
    # tlst = ['S1', 'S2', 'S3', 'S4']
    tlst = ['Z1', 'Z2', 'Z3', 'Z4']

    for topo, title in zip(topo_lst, tlst):

        plot_ps_by_different_algorithm(topo, alst, title=title)
    #
    # plot_ps_by_different_algorithm(topo='Rand1', algorithms=alst)
