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

import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def run(algorithm=None, runtime=None, problem=None):
    for i in range(runtime):
        if algorithm == 'NSGA-II':
            test = NSGA2(problem)
        elif algorithm == 'MOEAD':
            test = MOEAD(problem)
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

        start = time.time()
        tmp = test.run()
        end = time.time()
        logging.info("Run %s >>>>>> %s , ACT = %s s", test.name(),
                     str(i+1), str('%.2f' % (end - start)))
        write_list_to_json(topo=topo, algorithm=test.name(), runtime=i+1, solutions=tmp)

if __name__ == '__main__':
    path = '/Rand_Topo/'
    # path = '/SNDlib_Topo/'
    # path = '/Zoo_Topo/'
    topos = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topos = ['cost266', 'france', 'geant', 'germany50', 'india35',
    #          'newyork', 'pioro40','ta1', 'ta2']
    # topos = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica',
    #          'Chinanet', 'Dfn', 'Geant2012', 'HiberniaGlobal',
    #          'Highwinds', 'HurricaneElectric', 'Internetmci',
    #          'Rediris', 'Tinet', 'Uninett2011', 'Uunet']

    al_lst = ['NSACO', 'PBIL', 'MOPSO', 'NSGA-II', 'MOEAD', 'EAG-MOEAD', 'NSABC', 'SFLA-MOEAD', 'OBL-MOEAD']

    for topo in topos[2:3]:
        problem = MRP()
        problem.initialize(path=path, filename=topo)

        for al in al_lst[:1]:
            run(algorithm=al, runtime=10, problem=problem)

