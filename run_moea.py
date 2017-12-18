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

import time
import os

if __name__ == '__main__':

    topo = 'topo6'
    problem = MRP()
    problem.initialize(topo)
    #
    pf_list = []
    al_list = []
    for i in range(5):
        # test = MOEAD_SFLA(problem)
        test = MOEAD(problem)
        # test = NSGA2(problem)
        start = time.time()
        #
        tmp = test.run()
        end = time.time()
        print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
        write_list_to_json(topo, test.name(), i + 1, tmp)
        pf_list.extend(tmp)
    #
    # write_list_to_json(topo=topo, algorithm='MOEAD-SFLA', solutions=pf_list)
    write_list_to_json(topo=topo, algorithm='MOEAD', solutions=pf_list)
    # write_list_to_json(topo=topo, algorithm='NSGA-II', solutions=pf_list)
    #
    # al_list.append('MOEAD-SFLA')
    # al_list.append('MOEAD')
    # al_list.append('NSGA-II')
    # update_ideal_pf(topo=topo, algorithms=al_list, runtime=5)

