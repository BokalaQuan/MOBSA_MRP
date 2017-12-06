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


import time
import os

if __name__ == '__main__':
    
    topo = 'topo1'
    problem = MRP()
    problem.initialize(topo)
    
    pf_list = []
    for i in range(2):
        test = NSGA2(problem)
        start = time.time()
        tmp = test.run()
        end = time.time()
        print "Run >>>>>> ", i+1, ' ACT = ', end - start, ' s'
        pf_list.extend(tmp)
    
    write_list_to_json(topo, 'NSGA-II', pf_list)