from algorithm.individual import IndividualMRP
from algorithm.parameter import *
from algorithm.operator import fast_nondominated_sort
from moead import *

import random
import math
import numpy
import copy
import os

class MOEAD_SFLA(MultiObjectiveEvolutionaryAlgorithmBasedOnDecomposition):
    
    def __init__(self, problem):
        super(MOEAD_SFLA, self).__init__(problem)
        
        
    def name(self):
        return 'MOEAD-SFLA'
    
        
    def reproduction(self, ind):
        fit = []
        for i in ind.index_neighbor:
            fit.append(SubProblem.cal_fit(self.current_population[i].solution,
                                          ind.weight_vector, 'WS'))

            # fit.append(SubProblem.cal_fit(self.current_population[i].solution,
            #                               self.current_population[i].weight_vector, 'WS'))

        fit_worst = max(fit)
        index_worst = fit.index(fit_worst)
        sub_worst = self.current_population[index_worst]
        ind_worst = sub_worst.solution
        
        ind_new = ind_worst.copy()
        ind_new.mutation()
        ind_new.cal_fitness()
        # fit_new = SubProblem.cal_fit(ind_new, ind.weight_vector,
        #                              'TF', self.reference_point)

        fit_new = SubProblem.cal_fit(ind_new, ind.weight_vector, 'WS')
        # fit_new = SubProblem.cal_fit(ind_new, sub_worst.weight_vector, 'WS')

        if fit_new < fit_worst:
            return ind_new
        elif not ind_new >= ind_worst:
            ind_new.mutation()
            ind_new.cal_fitness()
            fit_new = SubProblem.cal_fit(ind_new, ind.weight_vector, 'WS')
            # fit_new = SubProblem.cal_fit(ind_new, sub_worst.weight_vector, 'WS')

            if fit_new < fit_worst:
                return ind_new
            else:
                ind_new = ind_worst.copy()
                ind_new.mutation()
                ind_new.cal_fitness()
                return ind_new
        else:
            ind1 = ind_worst.copy()
            ind2 = self.external_archive[random.randint(0, len(self.external_archive)-1)].copy()
            ind1.crossover(ind2)
            ind1.cal_fitness()
            return ind1
