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


import time
import os

if __name__ == '__main__':
    path = '/Rand_Topo/'
    # path = '/SNDlib_Topo/'
    # path = '/Zoo_Topo/'
    topos = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topos = ['cost266', 'france', 'geant', 'germany50', 'india35',
    #          'newyork', 'pioro40','ta1', 'ta2', 'zib54']
    # topos = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica',
    #          'Chinanet', 'Dfn', 'Geant2012', 'HiberniaGlobal',
    #          'Highwinds', 'HurricaneElectric', 'Internetmci',
    #          'Rediris', 'Tinet', 'Uninett2011', 'Uunet']

    for topo in topos[:]:
        print "TOPO is ", topo
        problem = MRP()
        problem.initialize(path=path, filename=topo)

        for i in range(20):
            test = NSGA2(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
            write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)


        for i in range(20):
            test = MOEAD(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
            write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)

        for i in range(20):
            test = EAG_MOEAD(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
            write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)

        for i in range(20):
            test = NSABC(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name(), " >>>>>> ", i + 1, ' ACT = ', end - start, ' s'
            write_list_to_json(topo=topo, algorithm=test.name(), runtime=i + 1, solutions=tmp)

        for i in range(20):
            test = MOEAD_SFLA(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
            write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)

        for i in range(20):
            test = MOEAD_OBL(problem)
            start = time.time()
            tmp = test.run()
            end = time.time()
            print "Run ", test.name()," >>>>>> ", i+1, ' ACT = ', end - start, ' s'
            write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)


