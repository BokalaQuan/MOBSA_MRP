"""
Adaptive Local Search Multi-objective Evolutionary Algorithm
Based on Decomposition.
"""

from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.operator import *
from algorithm.individual import IndividualMRP

import random
import numpy as np

class SubProblem(object):

    def __init__(self, weight_vector=None, solution=None, neighbor_size=None):
        self.weight_vector = weight_vector
        self.solution = solution
        self.neighbors = None
        self.neighbor_size = neighbor_size

    @staticmethod
    def cal_fit(ind=None, weight_vector=None, str_func_type=None, reference_point=None):
        fit = 0.0
        if str_func_type == 'WS':
            fit += weight_vector[0] * ind.fitness[0] + weight_vector[1] * ind.fitness[1]
        elif str_func_type == 'TF':
            x = weight_vector[0] * abs(ind.fitness[0] - reference_point[0])
            y = weight_vector[1] * abs(ind.fitness[1] - reference_point[1])
            fit = max(x, y)
        return fit

    def find_neighbors(self, str_func_type=None):
        if str_func_type == 'Chromosome':
            # for i in range(self.neighbor_size):
                pass



    def _func_chromosome(self, radius=None):
        changes_point = []
        while len(changes_point) < radius:
            p = random.randint(0, len(self.solution.chromosome) - 1)
            if p not in changes_point:
                changes_point.append(p)

        solution = self.solution.copy()
        for i in changes_point:
            solution.chromosome[i] = 1-solution.chromosome[i]
        solution.fitness = solution.cal_fitness()

        return solution






class AdaptiveLocalSearchMOEAD(MOEA):

    def __init__(self, problem):
        super(AdaptiveLocalSearchMOEAD, self).__init__(problem)

    def name(self):
        return 'MOEAD-ALS'

    def init_population(self):
        pass
