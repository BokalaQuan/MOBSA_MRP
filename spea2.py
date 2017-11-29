'''
Zitzler, et al.
"SPEA2: Improving the Strength Pareto Evolutionary Algorithm." (2001).
'''

from algorithm.individual import IndividualMRP
from algorithm.parameter import PM, PC, POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL, EXTERNAL_ARCHIVE_SIZE
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from algorithm.performance import cal_IGD, cal_GD, cal_HV
from algorithm.operator import object_shell_sort as shell_sort

import random
import copy
import math
import numpy

class IndividualSPEA(IndividualMRP):
    
    def __init__(self):
        super(IndividualSPEA, self).__init__()
        
        self.dominating_list = []
        self.dominated_list = []
        self.k_distance = 0.0
        self.strength = 0
        self.fit = 0.0
        
    
    def clear_property(self):
        self.dominating_list = []
        self.dominated_list = []
        self.strength = 0
        self.fit = 0.0
        
    def cal_fit(self):
        raw_fit = 0
        density = 1.0 / (self.k_distance + 2)
        
        for ind in self.dominated_list:
            raw_fit += ind.strength
            
        self.fit = raw_fit + density
        
    def is_fit_less(self, ind):
        if ind.fit > self.fit:
            return True
        return False
    

class SPEA2(object):
    
    def __init__(self, problem):
        self.problem = problem
        self.current_population = []
        self.external_archive = []
        
    def init_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualSPEA()
            ind.initialize(IndividualMRP.create_chromosome(self.problem.num_link), self.problem)
            self.current_population.append(ind)
            
    def fitness_assignment(self):
        union_population = []
        union_population.extend(self.current_population)
        union_population.extend(self.external_archive)
        
        k = int(math.sqrt(len(union_population)))
        distance_matrix = []
        for ind0 in union_population:
            distance = []
            for ind1 in union_population:
                distance.append(numpy.linalg.norm(numpy.mat(ind0.fitness) - numpy.mat(ind1.fitness)))
            distance_matrix.append(distance_matrix)
            
        for dis, ind in zip(distance_matrix, union_population):
            ind.k_distance = dis.sort()[k]
            ind.clear_property()
            
        self.current_population = []
        self.external_archive = []
        
        for ind0 in union_population:
            for ind1 in union_population:
                if ind0.is_dominated(ind1):
                    ind1.strength += 1
                    ind0.dominated_list.append(ind1)
                elif ind1.is_dominated(ind0):
                    ind0.strength += 1
                    ind1.dominated_list.append(ind0)
                    
        for ind in union_population:
            ind.cal_fit()
            
        return shell_sort(union_population, 'fit')
    
    def environment_select(self, union_list):
        for i in range(len(union_list)-1, -1, -1):
            if union_list[i].fit < 1:
                self.external_archive.append(union_list.pop(i))
                
        if len(self.external_archive) < EXTERNAL_ARCHIVE_SIZE:
            num = EXTERNAL_ARCHIVE_SIZE - len(self.external_archive)
            for i in range(-1, -num-1, -1):
                self.external_archive.append(union_list.pop(i))
        elif len(self.external_archive) > EXTERNAL_ARCHIVE_SIZE:
            pass
        
        
        
if __name__ == '__main__':
    
    l = range(10)
    ll = []
    
    for i in range(len(l)-1, -1, -1):
        if l[i] > 5:
            ll.append(l.pop(i))
        
    print l
    print ll
        
        
        
    









