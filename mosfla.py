'''
@author A. H-P, et al.
@title "MOSFLA-MRPP: Multi-Objective Shuffled Frog-Leaping Algorithm applied
        to Mobile Robot Path Planning"
@date 2015
'''

from algorithm.parameter import *
from algorithm.operator import *
from nsga2 import IndividualNSGA

import random
import copy

class IndividualSFLA(IndividualNSGA):
    
    def __init__(self):
        super(IndividualSFLA, self).__init__()
        self.mofitness = 0
        
    def cal_mofitness(self):
        self.mofitness = 1 / (2 ** self.pareto_rank + 1 / (1 + self.crowding_distance))
    
    def copy(self):
        ind = IndividualSFLA()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)
        ind.paths = copy.deepcopy(self.paths)
        ind.delay = self.delay
        ind.loss = self.loss
        ind.bandwidth = self.bandwidth
        
        return ind
    
    
class Memeplex(object):
    
    def __init__(self, memeplex_size):
        self.memeplex_size = memeplex_size
        self.solutions = []
    
    def initialize(self, problem):
        for i in range(self.memeplex_size):
            ind = IndividualSFLA()
            ind.init_ind(problem)
            self.solutions.append(ind)
        
    def local_search(self):
        ind_worst = self.solutions.pop(-1)
        ind_mutate = ind_worst.copy()
        ind_mutate.mutation()
        
        if ind_worst.is_dominated(ind_mutate):
            self.solutions.append(ind_mutate)
            
        elif not ind_mutate.is_dominated(ind_worst):
            new_mutate = ind_mutate.copy()
            new_mutate.mutation()
            
            if ind_worst.is_dominated(new_mutate):
                self.solutions.append(new_mutate)
            else:
                new_ind = IndividualSFLA()
                new_ind.init_ind(ind_worst.problem)
                self.solutions.append(new_ind)
                
        else:
            ind_mutate = ind_worst.copy()
            ind_mutate.mutation()
            
            if  ind_worst.is_dominated(ind_mutate):
                self.solutions.append(ind_mutate)
            else:
                new_ind = IndividualSFLA()
                new_ind.init_ind(ind_worst.problem)
                self.solutions.append(new_ind)


class MultiObjectiveShuffledFrogLeapingAlgorithm(object):
    
    def __init__(self, problem, num_memeplex):
        self.problem = problem
        self.num_memeplex = num_memeplex
        self.iter_memeplex = POPULATION_SIZE / num_memeplex
        self.memeplexes = []
        self.current_population = []
        self.external_archive = []
    
    def name(self):
        return 'MOSFLA'
    
    def init_population(self):
        for i in range(self.num_memeplex):
            memeplex = Memeplex(POPULATION_SIZE / self.num_memeplex)
            memeplex.initialize(self.problem)
            self.current_population.extend(memeplex.solutions)
    
    def divide_into_memeplex(self):
        for mple in self.memeplexes:
            mple.solutions = []
        
        for i in range(POPULATION_SIZE):
            for j in range(self.num_memeplex):
                if i / self.num_memeplex == j:
                    self.memeplexes[j].solutions.append(self.current_population[i].copy())
        
    def merge_into_population(self):
        self.current_population = []
        for mmp in self.memeplexes:
            self.current_population.extend(mmp.solutions)

    def update_archive(self):
        union_set = []
        union_set.extend(self.current_population)
        union_set.extend(self.external_archive)
        
        self.external_archive = []
        self.external_archive.extend(fast_nondominated_sort(union_set)[0])
        
    def run(self):
        pass
    
    

