#!/usr/bin/env python
# -*-coding:utf-8 -*-

from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from algorithm.util import *

from nsga2 import NondominatedSortGeneticAlgorithm2 as NSGA2
from moead import MultiObjectiveEvolutionaryAlgorithmBasedOnDecomposition as MOEAD
from mopbil import MultiObjectivePopulationBasedIncrementalLearning as MOPBIL
from mopbil import PopulationBasedIncrementalLearning as PBIL
from mopso import MultiObjectiveParticleSwarmOptimization as MOPSO
from mosfla import MultiObjectiveShuffledFrogLeapingAlgorithm as MOSFLA
from spea2 import StrengthParetoEvolutionaryAlgorithm2 as SPEA2
from mobsa import MultiObjectiveBeetleSearchAlgorithm as MOBSO
from eag_moead import ExternalArchiveGuidedMOEAD as EAG_MOEAD
from moead_sfla import MOEAD_SFLA
from moead_obl import MOEAD_OBL
from nsabc import NondominatedSortingArtificialBeeColony as NSABC
from nsaco import NSACO
from jaya import Jaya
from ACO_M import ACO
from INSGA2 import INSGA2
from moea_pcg import MOEAPCG
from sfla import MOEAD_SFLA as MOSFLA

import time
import sys
import logging


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

def run(topo=None, algorithm=None, runtime=None, problem=None):
    test = None
    for i in range(runtime):
        if algorithm == 'NSGA-II':
            test = NSGA2(problem)
        elif algorithm == 'MOEAD':
            test = MOEAD(problem)
        elif algorithm == 'MOPBIL':
            test = MOPBIL(problem)
        elif algorithm == 'SPEA2':
            test = SPEA2(problem)
        elif algorithm == 'EAG-MOEAD':
            test = EAG_MOEAD(problem)
        elif algorithm == 'NSABC':
            test = NSABC(problem)
        elif algorithm == 'SFLA-MOEAD':
            test = MOEAD_SFLA(problem)
        elif algorithm == 'OBL-MOEAD':
            test = MOEAD_OBL(problem)
        elif algorithm == 'MOPSO':
            test = MOPSO(problem)
        elif algorithm == 'PBIL':
            test = PBIL(problem)
        elif algorithm == 'NSACO':
            test = NSACO(problem)
        elif algorithm == 'Jaya':
            test = Jaya(problem)
        elif algorithm == 'ACO':
            test = ACO(problem)
        elif algorithm == 'ENS-NDT':
            test = INSGA2(problem)
        elif algorithm == 'MOEA-PCG':
            test = MOEAPCG(problem)
        elif algorithm == 'MOSFLA':
            test = MOSFLA(problem)

        start = time.time()
        tmp = test.run()
        end = time.time()
        logger.info("Run %s >>>>>> %s , ACT = %s s", test.name(),
                     str(i+1), str('%.2f' % (end - start)))
        write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)

    test.show()

if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
    fh = logging.FileHandler('Record_RunMOEA.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(FORMAT)
    logger.addHandler(fh)

    lst = sys.argv[:]

    path = PATHs[lst[1]]

    topo_lst = lst[3 : 3+int(lst[2])]
    al_lst = lst[4+int(lst[2]) : 4+int(lst[2])+int(lst[3+int(lst[2])])]
    runtime = int(lst[-1])

    print(lst)
    print(topo_lst)
    print(al_lst)
    print(runtime)
    #
    # path = PATHs['Rand']
    # topo_lst = ['Rand1']
    # al_lst = ['Jaya']
    # runtime = 1


    for topo in topo_lst:
        problem = MRP()
        problem.initialize(path=path, filename=topo)
        for al in al_lst:

            run(topo=topo, algorithm=al, runtime=runtime, problem=problem)


