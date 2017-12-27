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


import time
import os

if __name__ == '__main__':
    topos = ['topo1', 'topo2', 'topo3', 'topo4', 'topo5', 'topo6']
    for topo in topos:
        print "TOPO is ", topo
        problem = MRP()
        problem.initialize(topo)

        for i in range(20):
            test = NSGA2(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
        write_list_to_json(topo, test.name(), i+1, tmp)

        for i in range(20):
            test = MOEAD(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
        write_list_to_json(topo, test.name(), i+1, tmp)

        for i in range(20):
            test = MOEAD_SFLA(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
        write_list_to_json(topo, test.name(), i+1, tmp)

        for i in range(20):
            test = MOEAD_OBL(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
        write_list_to_json(topo, test.name(), i+1, tmp)


















