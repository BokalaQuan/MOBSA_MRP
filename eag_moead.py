"""
@author Xinye Cai, et al.
@title "An External Archive Guided Multiobjective Evolutionary Algorithm Based on Decomposition for Combinatorial Optimization."
@date 2015
"""

from moead import WeightVector, SubProblem
from algorithm.parameter import *
from nsga2 import IndividualNSGA
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.operator import fast_nondominated_sort, crowding_distance_sort

import random
import math
import numpy as np
import matplotlib.pyplot as plt


class SubProblemEAG(SubProblem):
    def __init__(self, weight_vector=None, index_neighbor=None, solution=None):
        '''
        init instance of SubProblem in EAG-MOEA/D
        :param weight_vector:
        :param index_neighbor:
        :param solution:
        '''
        super(SubProblemEAG, self).__init__(weight_vector, index_neighbor, solution)
        self.set_of_success = []
        self.set_of_solutions = []


class ExternalArchiveGuidedMOEAD(MOEA):
    def __init__(self, problem=None):
        super(ExternalArchiveGuidedMOEAD, self).__init__(problem)
        self.L = int(math.sqrt(MAX_NUMBER_FUNCTION_EVAL))

    def name(self):
        return 'EAG-MOEAD'

    def init_population(self):
        vectors = WeightVector(int(math.sqrt(POPULATION_SIZE)))
        vectors.initialize_vector()
        for i in range(POPULATION_SIZE):
            ind = IndividualNSGA()
            ind.init_ind(self.problem)

            sub_sol = SubProblemEAG(weight_vector=vectors.weight_vector[i],
                                    index_neighbor=vectors.index_neighbor[i],
                                    solution=ind)

            self.current_population.append(sub_sol)
            self.external_archive.append(ind.copy())

    def evaluate_population(self, gen=None):
        S_list = []
        for sub in self.current_population:
            S_list.append(sum(sub.set_of_success[gen - self.L:]))
            sub.set_of_solutions = []

        tmp = sum(S_list) + 0.02
        D_list = [float(s / tmp) for s in S_list]
        P_list = [sum(D_list[:i + 1]) for i in range(POPULATION_SIZE)]

        return P_list

    def select_subproblem(self, p_list):
        select_ind = None
        p_sel = random.uniform(0, 1)

        if p_sel <= p_list[0]:
            select_ind = self.current_population[0]
        else:
            for i in range(1, POPULATION_SIZE):
                if p_sel > p_list[i - 1] and p_sel <= p_list[i]:
                    select_ind = self.current_population[i]
                    break

        return select_ind

    def reproduction(self, ind):
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, len(ind.index_neighbor) - 1)
            index2 = random.randint(0, len(ind.index_neighbor) - 1)

        ind1 = self.current_population[ind.index_neighbor[index1]].solution.copy()
        ind2 = self.current_population[ind.index_neighbor[index2]].solution.copy()

        if random.uniform(0, 1) < PC:
            ind1.crossover(ind2)

        ind1.mutation()
        ind2.mutation()

        if ind1 >= ind2:
            ind_new = ind2
        elif ind1 <= ind2:
            ind_new = ind1
        else:
            ind_new = ind1 if random.uniform(0, 1) < 0.5 else ind2

        ind.set_of_solutions.append(ind_new)

        return ind_new

    def update_neighbor_solution(self, ind):
        for i in ind.index_neighbor:
            ind_select = self.current_population[i]

            for sol in ind.set_of_solutions:
                fit1 = ind.cal_fit(sol, ind_select.weight_vector, 'WS')
                fit2 = ind.cal_fit(ind_select.solution, ind_select.weight_vector, 'WS')

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

    def run(self):
        # test
        plt.figure()

        self.init_population()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            if gen < self.L:
                select_sub = self.current_population
            else:
                P_list = self.evaluate_population(gen=gen)
                select_sub = [self.select_subproblem(P_list) for i in range(POPULATION_SIZE)]

            new_solutions = [self.reproduction(sub) for sub in select_sub]

            for sub in set(select_sub):
                self.update_neighbor_solution(sub)

            self.update_archive(new_solutions)
            gen += 1

            data = [ind.fitness for ind in self.external_archive]
            tmp = np.array(data)
            plt.scatter(tmp[:, 0], tmp[:, 1], alpha=0.5)

        plt.xlabel('Ave_plr (%)', fontsize=12)
        plt.ylabel('Ave_delay (ms)', fontsize=12)
        plt.legend('EAG-MOEA/D', fontsize=10)
        plt.show()

        return self.external_archive
