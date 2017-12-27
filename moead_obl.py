from algorithm.individual import IndividualMRP
from algorithm.parameter import *
from algorithm.operator import fast_nondominated_sort
from moead import *
from nsga2 import IndividualNSGA

import random
import math
import numpy
import copy
import os


class MOEAD_OBL(MultiObjectiveEvolutionaryAlgorithmBasedOnDecomposition):
    def __init__(self, problem):
        super(MOEAD_OBL, self).__init__(problem)

    def name(self):
        return 'MOEAD-OBL'

    def init_population(self):
        vectors = WeightVector(int(math.sqrt(POPULATION_SIZE)))
        vectors.initialize_vector()
        for i in range(POPULATION_SIZE):
            ind = IndividualNSGA()
            ind.init_ind(self.problem)

            sub_sol = SubProblem(weight_vector=vectors.weight_vector[i],
                                 index_neighbor=vectors.index_neighbor[i],
                                 solution=ind)

            self.current_population.append(sub_sol)
            self.update_archive(ind)

    def reproduction(self, ind):
        fit = []
        for i in ind.index_neighbor:
            fit.append(SubProblem.cal_fit(self.current_population[i].solution,
                                          ind.weight_vector, 'WS'))
        #         # fit.append(SubProblem.cal_fit(self.current_population[i].solution,
            #                               self.current_population[i].weight_vector, 'WS'))
    #
        fit_worst = max(fit)
        index_worst = fit.index(fit_worst)
        sub_worst = self.current_population[index_worst]
        ind_worst = sub_worst.solution
    #
        ind_new = ind_worst.copy()
        ind_new.mutation()
        ind_new.fitness = ind_new.cal_fitness()
        # fit_new = SubProblem.cal_fit(ind_new, ind.weight_vector,
        #                              'TF', self.reference_point)
    #
        fit_new = SubProblem.cal_fit(ind_new, ind.weight_vector, 'WS')
        # fit_new = SubProblem.cal_fit(ind_new, sub_worst.weight_vector, 'WS')
    #
        if fit_new < fit_worst:
            return ind_new
        elif not ind_new >= ind_worst:
            ind_new.mutation()
            ind_new.fitness = ind_new.cal_fitness()
            fit_new = SubProblem.cal_fit(ind_new, ind.weight_vector, 'WS')
            # fit_new = SubProblem.cal_fit(ind_new, sub_worst.weight_vector, 'WS')
    #
            if fit_new < fit_worst:
                return ind_new
            else:
                ind_new = ind_worst.copy()
                ind_new.mutation()
                ind_new.fitness = ind_new.cal_fitness()
                return ind_new
        else:
            ind1 = ind_worst.copy()
            ind2 = self.external_archive[random.randint(0, len(self.external_archive) - 1)].copy()
            ind1.crossover(ind2)
            ind1.fitness = ind1.cal_fitness()
            return ind1

    def elite_opposition_based_learning(self):
        obl_list = []
        for ind in self.external_archive:
            obl_list.append(ind.opposition_based_learning())

        union_list = []
        union_list.extend(self.external_archive)
        union_list.extend(obl_list)

        self.external_archive = fast_nondominated_sort(union_list)[0]

    def run(self):
        self.init_population()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            for ind in self.current_population:
                new_solution = self.reproduction(ind)
                # self.update_reference_point(new_solution)
                self.update_neighbor_solution(new_solution, ind)
                self.update_archive(new_solution)
            self.elite_opposition_based_learning()
            gen += 1

        return self.external_archive
