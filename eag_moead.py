"""
@author Xinye Cai, et al.
@title "An External Archive Guided Multiobjective Evolutionary Algorithm Based on Decomposition for Combinatorial Optimization."
@date 2015
"""

from moead import WeightVector, SubProblem
from algorithm.parameter import POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL, PC, EXTERNAL_ARCHIVE_SIZE, INF
from algorithm.individual import IndividualMRP
from algorithm.operator import fast_nondominated_sort, crowding_distance_sort

import random
import copy
import numpy

class SubProblemEAG(SubProblem):
    
    def __init__(self, weight_vector=None, index_neighbor=None, solution=None):
        '''
        init instance of SubProblem in EAG-MOEA/D
        :param weight_vector:
        :param index_neighbor:
        :param solution:
        '''
        super(SubProblemEAG, self).__init__(weight_vector, index_neighbor, solution)
        self.S = 0
        self.D = float(0)
        self.P_select = float(1)
        self.set_of_success = []
        self.set_of_solutions = []
        
    
    def cal_S(self, gen=None):
        '''
        S :-> the number of successful solutions generated.
        :return:
        '''
        # L = 8
        self.S = sum(self.set_of_success[gen - 8:])
    
    def cal_D(self, poplist=None):
        '''
        D :-> the proportion of successful solution generated.
        :param poplist:
        :return:
        '''
        tmp = 0
        for pop in poplist:
            tmp += pop.S
        # epsilon = 0.002
        self.D = self.S / tmp + 0.002
        
    def cal_P(self, poplist=None):
        '''
        P :-> the probability of selecting Subproblem
        :param poplist:
        :return:
        '''
        tmp = 0
        for pop in poplist:
            tmp += pop.D
            
        self.P_select = self.D / tmp
        
    def clear_property(self):
        self.set_of_success = []
        
        
class ExternalArchiveGuidedMOEAD(object):
    
    def __init__(self, problem=None):
        self.problem = problem
        self.current_population = []
        self.external_archive = []
    
    def name(self):
        return 'EAG-MOEAD'
        
    def init_population(self):
        vectors = WeightVector(POPULATION_SIZE/10)
        vectors.initialize_vector()
        for i in range(POPULATION_SIZE):
            ind = IndividualMRP()
            ind.initialize(IndividualMRP.create_chromosome(self.problem.num_link), self.problem)
            
            sub_sol = SubProblemEAG(weight_vector=vectors.weight_vector[i],
                                 index_neighbor=vectors.index_neighbor[i],
                                 solution=ind)
            self.current_population.append(sub_sol)
            self.external_archive.append(ind.copy())
    
    def select_subproblem(self):
        p_sel = random.uniform(0, 1)
        if p_sel <= self.current_population[0].P_select:
            return self.current_population[0]
        
        for i in range(1, POPULATION_SIZE):
            if p_sel <= self.current_population[i] and \
                p_sel > self.current_population[i-1]:
                return self.current_population[i]
            
    def generate_new_solution(self, ind):
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, len(ind.index_neighbor)-1)
            index2 = random.randint(0, len(ind.index_neighbor)-1)

        ind1 = self.current_population[ind.index_neighbor[index1]].solution.copy()
        ind2 = self.current_population[ind.index_neighbor[index2]].solution.copy()

        if random.random() < PC:
            ind1.crossover(ind2)

        ind1.mutation()
        ind2.mutation()

        if ind1.is_dominated(ind2):
            ind.set_of_solutions.append(ind2)
            ind_new = ind2
        elif ind2.is_dominated(ind1):
            ind.set_of_solutions.append(ind1)
            ind_new = ind1
        else:
            if random.random() < 0.5:
                ind.set_of_solutions.append(ind1)
                ind_new = ind1
            else:
                ind.set_of_solutions.append(ind2)
                ind_new = ind2
        
        return ind_new
                
        
    def update_neighbor(self, ind):
        for i in ind.index_neighbor:
            ind_select = self.current_population[i]
            
            for sol in ind.set_of_solutions:
                fit1 = ind.cal_fit(sol, ind_select.weight_vector,
                                   'WS', reference_point=None)
                fit2 = ind.cal_fit(ind_select.solution, ind_select.weight_vector,
                                   'WS', reference_point=None)
            
                if fit1 < fit2:
                    ind_select.solution = sol.copy()
        
    
    def update_archive(self, new_solutions):
        union_set = []
        union_set.extend(new_solutions)
        union_set.extend(self.external_archive)

        pareto_rank_set_list = fast_nondominated_sort(union_set)
        crowding_distance_sort(pareto_rank_set_list)
        
        self.external_archive = []
        for pareto_rank_set in pareto_rank_set_list:
            if len(self.external_archive) < POPULATION_SIZE:
                if (len(pareto_rank_set) + len(self.external_archive)) <= POPULATION_SIZE:
                    for ind in pareto_rank_set:
                        self.external_archive.append(ind)
                else:
                    current = len(self.external_archive)
                    for i in range(POPULATION_SIZE - current):
                        self.external_archive.append(pareto_rank_set[i])
        
        for ind in self.current_population:
            num_success = 0
            for sol in ind.set_of_solutions:
                if sol in self.external_archive:
                    num_success += 1
            ind.set_of_success.append(num_success)
        
    
    def main(self):
        pass
    

if __name__ == '__main__':
    
    pass
    
    
    
