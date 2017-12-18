from moead import WeightVector, SubProblem
from mopbil import ProbabilityVector as PV
from algorithm.parameter import POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL, INF
from algorithm.individual import IndividualMRP

import random
import copy
import math

class Candidate(IndividualMRP):
    
    def __init__(self):
        super(Candidate, self).__init__()
        self.state = False
        

class SubPopulation(object):
    
    def __init__(self, pv, sub_problem, problem):
        self.problem = problem
        self.pv = pv
        self.sub_problem = sub_problem
        
        self.tabu_set = []
        self.tabu_len = None
        self.candidates = []
        self.neighbors = []
        
    def init_subpop(self):
        for i in range(int(math.sqrt(POPULATION_SIZE))):
            ind = Candidate()
            ind.initialize(self.pv.generate_chromosome(), self.problem)
            self.neighbors.append(ind)
        
    def tabu_search_in_subpop(self):
        for i in range(int(math.sqrt(POPULATION_SIZE))):
            pass
        
    
    


class ALMOEAD(object):
    '''
    Augmented Learning Multi-Objective Evolutionary Algorithm Based on Decomposition
    '''
    def __init__(self):
        pass
    