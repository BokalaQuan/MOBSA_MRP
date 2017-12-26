from problem.kp.knapsack_problem import MultiObjectiveKnapsackProblem as MOKP
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

import os
import time


if __name__ == '__main__':

    ins = '50_2.json'
    problem = MOKP()
    problem.initialize(ins)

    pf_list = []
    al_list = []

    for i in range(10):
        test = MOEAD(problem=problem)
        start = time.time()
        tmp = test.run()
        end = time.time()

        print "Run ", test.name(), " >>> ", i+1, " ACT = ", end-start, ' s'
