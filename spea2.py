'''
@author Zitzler, et al.
@title "SPEA2: Improving the Strength Pareto Evolutionary Algorithm."
@date 2001.
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
        
    
    def clear_dominated_property(self):
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
        

class StrengthParetoEvolutionaryAlgorithm2(object):
    
    def __init__(self, problem):
        self.problem = problem
        self.current_population = []
        self.external_archive = []
        
    def name(self):
        return 'SPEA2'
    
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
            distance_matrix.append(distance)
            
        for dis, ind in zip(distance_matrix, union_population):
            dis.sort()
            ind.k_distance = dis[k]
            ind.clear_dominated_property()
            
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
            for i in range(len(self.external_archive)-1):
                for j in range(i+1, len(self.external_archive)):
                    if self.external_archive[i].is_euqal(self.external_archive[j]):
                        self.external_archive.pop(j)
        
    def selection_evolution(self):
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, POPULATION_SIZE-1)
            index2 = random.randint(0, POPULATION_SIZE-1)
    
        ind1 = self.external_archive[index1]
        ind2 = self.external_archive[index2]
    
        if ind1.fit > ind2.fit:
            self.current_population.append(ind2.copy())
        else:
            self.current_population.append(ind1.copy())
            
        for i in range(POPULATION_SIZE/2):
            if random.random() < PC:
                self.current_population[i].crossover(self.current_population[POPULATION_SIZE-i-1])
        
        for ind in self.current_population:
            ind.mutation()
            
    def run(self):
        self.init_population()
        
        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            temp_list = self.fitness_assignment()
            self.environment_select(temp_list)
            self.selection_evolution()
            gen += 1


if __name__ == '__main__':
    
    pass
        
    









