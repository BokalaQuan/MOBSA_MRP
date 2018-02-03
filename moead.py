"""
@author Zhang, Qingfu, and H. Li.
@title "MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition."
@date 2007
"""

from algorithm.individual import IndividualMRP
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *

import random
import copy
import numpy
import math

class WeightVector(object):

    def __init__(self, NumOfNeighbor=None):
        self.weight_vector = []
        self.index_neighbor = []
        self.H = float(POPULATION_SIZE - 1)
        self.N = POPULATION_SIZE
        self.T = NumOfNeighbor
        
    def create_weight_vector(self):
        '''
        @function for create N weight vectors.
        :return:
        '''
        # lambda vector
        lv = numpy.array(range(0, self.N)) / self.H
        for i in range(self.N):
            vector = [lv[i], lv[self.N - i - 1]]
            self.weight_vector.append(vector)
    
    def create_neighborhood(self):
        '''
        @function for create each vector's neighbors,
        due to the distance od two vector
        :return:
        '''
        for vec in self.weight_vector:
            neighbor = []
            distance = []
            for tem in self.weight_vector:
                distance.append(numpy.linalg.norm(numpy.array(vec) - numpy.array(tem)))
            
            temp = copy.copy(distance)
            temp.sort()
            
            for i in range(self.T):
                neighbor.append(distance.index(temp[i]))
                distance[distance.index((temp[i]))] = 12
            
            self.index_neighbor.append(neighbor)
    
    def initialize_vector(self):
        self.create_weight_vector()
        self.create_neighborhood()


class SubProblem(object):
    
    def __init__(self, weight_vector=None, index_neighbor=None, solution=None):
        '''
        
        :param weight_vector:
        :param index_neighbor:
        :param solution:
        '''
        self.weight_vector = weight_vector
        self.index_neighbor = index_neighbor
        self.solution = solution
    
    @staticmethod
    def cal_fit(ind=None, weight_vector=None, str_func_type=None, reference_point=None):
        '''
        @method Weighted Sum Approach, key='WS'
        @method Tchebycheff Approach, key='TF'
        :param ind:
        :param weight_vector:
        :param str_func_type:
        :param reference_point:
        :return:
        '''
        fit = 0.0
        if str_func_type == 'WS':
            fit += weight_vector[0] * ind.fitness[0] + weight_vector[1] * ind.fitness[1]
        elif str_func_type == 'TF':
            x = weight_vector[0] * abs(ind.fitness[0] - reference_point[0])
            y = weight_vector[1] * abs(ind.fitness[1] - reference_point[1])
            fit = max(x, y)
        return fit


class MultiObjectiveEvolutionaryAlgorithmBasedOnDecomposition(MOEA):
    
    def __init__(self, problem):
        super(MultiObjectiveEvolutionaryAlgorithmBasedOnDecomposition, self).__init__(problem)
        self.reference_point = [INF, INF]
    
    def name(self):
        return 'MOEAD'
    
    def init_population(self):
        vectors = WeightVector(int(math.sqrt(POPULATION_SIZE)))
        vectors.initialize_vector()
        for i in range(POPULATION_SIZE):
            ind = IndividualMRP()
            ind.init_ind(self.problem)
            
            sub_sol = SubProblem(weight_vector=vectors.weight_vector[i],
                                 index_neighbor=vectors.index_neighbor[i],
                                 solution=ind)
            
            self.current_population.append(sub_sol)
            self.update_archive(ind)
            # self.update_reference_point(ind)
    
    def update_archive(self, ind):
        if len(self.external_archive) == 0:
            self.external_archive.append(ind)
        else:
            flag = 0
            for sol in self.external_archive[:]:
                if ind <= sol:
                    self.external_archive.remove(sol)
                elif ind >=sol or ind == sol:
                    flag += 1
            if flag == 0:
                self.external_archive.append(ind)
                

    def update_reference_point(self, ind):
        tmp = []
        for fit, ref in zip(ind.fitness, self.reference_point):
            tmp.append(min(fit, ref))
        self.reference_point = tmp
    
    def reproduction(self, ind):
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, len(ind.index_neighbor)-1)
            index2 = random.randint(0, len(ind.index_neighbor)-1)
        
        ind1 = self.current_population[ind.index_neighbor[index1]].solution.copy()
        ind2 = self.current_population[ind.index_neighbor[index2]].solution.copy()
        
        if random.uniform(0, 1) < PC:
            ind1.crossover(ind2)
        
        ind1.mutation()
        ind2.mutation()
        
        ind1.cal_fitness()
        ind2.cal_fitness()
        
        if ind1 >= ind2:
            return ind2
        elif ind1 <= ind2:
            return ind1
        else:
            return ind1 if random.random() < 0.5 else ind2
    
    def update_neighbor_solution(self, new_solution, ind):
        for i in ind.index_neighbor:
            ind_select = self.current_population[i]

            fit1 = SubProblem.cal_fit(new_solution, ind_select.weight_vector, 'WS')
            fit2 = SubProblem.cal_fit(ind_select.solution, ind_select.weight_vector, 'WS')

            if fit1 < fit2:
                ind_select.solution = new_solution
    
    def run(self):
        self.init_population()
        
        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            for ind in self.current_population:
                new_solution = self.reproduction(ind)
                # self.update_reference_point(new_solution)
                self.update_neighbor_solution(new_solution, ind)
                self.update_archive(new_solution)
            gen += 1
        
        return self.external_archive
