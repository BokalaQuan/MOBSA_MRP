'''
@author Zitzler, et al.
@title "SPEA2: Improving the Strength Pareto Evolutionary Algorithm."
@date 2001.
'''

from algorithm.individual import IndividualMRP
from algorithm.parameter import *
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA

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

    def copy(self):
        ind = IndividualSPEA()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)
        ind.paths = copy.deepcopy(self.paths)
        ind.delay = self.delay
        ind.loss = self.loss
        ind.bandwidth = self.bandwidth
        return ind
        
    def cal_fit(self):
        raw_fit = 0
        density = 1.0 / (self.k_distance + 2)
        
        for ind in self.dominated_list:
            raw_fit += ind.strength
            
        self.fit = raw_fit + density

def cal_distance_matrix(poplist):
    distance_matrix = []
    for ind0 in poplist:
        distance = []
        for ind1 in poplist:
            distance.append(numpy.linalg.norm(numpy.mat(ind0.fitness) -
                                              numpy.mat(ind1.fitness)))
        distance_matrix.append(distance)

    return numpy.array(distance_matrix)

class StrengthParetoEvolutionaryAlgorithm2(MOEA):
    
    def __init__(self, problem):
        super(StrengthParetoEvolutionaryAlgorithm2, self).__init__(problem)
        
    def name(self):
        return 'SPEA2'
    
    def init_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualSPEA()
            ind.init_ind(self.problem)
            self.current_population.append(ind)

    def fitness_assignment(self):
        union_population = []
        union_population.extend(self.current_population)
        union_population.extend(self.external_archive)

        dis_mx = cal_distance_matrix(union_population)
        dis_mx.sort(axis=1)

        k = int(math.sqrt(len(union_population)))

        for ind, dis in zip(union_population, dis_mx):
            ind.k_distance = dis[k]
            ind.clear_dominated_property()

        self.current_population = []
        self.external_archive = []
        
        for ind0 in union_population:
            for ind1 in union_population:
                if ind0 >= ind1:
                    ind1.strength += 1
                    ind0.dominated_list.append(ind1)
                elif ind0 <= ind1:
                    ind0.strength += 1
                    ind1.dominated_list.append(ind0)
                    
        for ind in union_population:
            ind.cal_fit()
            
        union_population.sort(cmp=None, key=lambda x:x.fit, reverse=True)
        return union_population
    
    def environment_select(self, union_list):
        for i in range(len(union_list)-1, -1, -1):
            if union_list[i].fit < 1:
                self.external_archive.append(union_list.pop(i))

        if len(self.external_archive) < POPULATION_SIZE:
            while len(self.external_archive) < POPULATION_SIZE:
                self.external_archive.append(union_list.pop(-1))
        elif len(self.external_archive) > POPULATION_SIZE:
            dis_mx = cal_distance_matrix(self.external_archive)

            while len(self.external_archive) > POPULATION_SIZE:
                distance_matrix = copy.copy(dis_mx)
                distance_matrix.sort(axis=1)

                min_dis = float('inf')
                min_index = -1

                for i in range(len(distance_matrix)):
                    dis = distance_matrix[i]
                    point = dis[1]

                    if point < min_dis:
                        min_dis = point
                        min_index = i
                    elif point == min_dis:
                        for j in range(len(dis)):
                            k1 = dis[j]
                            k2 = distance_matrix[min_index][j]

                            if k1 < k2:
                                min_index = i
                                break
                            elif k1 > k2:
                                break

                self.external_archive.pop(min_index)
                dis_mx = numpy.delete(dis_mx, min_index, axis=1)
                dis_mx = numpy.delete(dis_mx, min_index, axis=0)

    def envrionmental_selection(self, union_list):
        for i in range(len(union_list)-1, -1, -1):
            if union_list[i].fit < 1:
                self.external_archive.append(union_list.pop(i))

        if len(self.external_archive) < POPULATION_SIZE:
            while len(self.external_archive) < POPULATION_SIZE:
                self.external_archive.append(union_list.pop(-1))
        elif len(self.external_archive) > POPULATION_SIZE:
            N = len(self.external_archive) - POPULATION_SIZE
            tmp = 0
            while tmp < N:
                for index, ind in enumerate(self.external_archive):
                    for sel in self.external_archive[index+1:]:
                        if ind == sel and tmp < N:
                            self.external_archive.remove(sel)
                            tmp += 1

                        if tmp >= N:
                            break

                    if tmp >= N:
                        break

    def selection_evolution(self):
        while len(self.current_population) < POPULATION_SIZE:
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
            if random.uniform(0, 1) < PC:
                self.current_population[i].crossover(self.current_population[POPULATION_SIZE-i-1])
        
        for ind in self.current_population:
            ind.mutation()
            ind.fitness = ind.cal_fitness()
            
    def run(self):
        self.init_population()
        
        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            temp_list = self.fitness_assignment()
            # self.environment_select(temp_list)
            self.envrionmental_selection(temp_list)
            self.selection_evolution()
            print "Gen = ", gen, " POPSIZE = ", len(self.current_population), " ARCHIVE SIZE = ", len(self.external_archive)

            gen += 1

        return self.external_archive