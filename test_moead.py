from moead import WeightVector, SubProblem
from mopbil import ProbabilityVector as PV
from algorithm.parameter import POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL, INF
from algorithm.individual import IndividualMRP

import random
import copy

class Candidate(IndividualMRP):
    
    def __init__(self):
        super(Candidate, self).__init__()
        self.state = False
        

class SubPopulation(object):
    
    def __init__(self, pv, sub_problem):
        self.pv = pv
        self.sub_problem = sub_problem
        
        self.tabu_set = []
        self.tabu_len = None
        self.candidates = []
        
    def init_subpop(self):
        pass
        
    
    def tabu_search_in_subpop(self):
        pass
    
    
    