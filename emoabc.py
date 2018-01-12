"""
@author Avadh Kishor, et al.
@title "NSABC: Non-dominated sorting based multi-objective artificial bee colony
        algorithm and its application in data clustering."
@date 2016
"""

from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.util import func_trans_S1 as func
from algorithm.operator import *
from nsga2 import IndividualNSGA

import random
import numpy as np
import copy

X_MIN = -3.0
X_MAX = 3.0


class IndividualABC(IndividualNSGA):

    def __init__(self):
        super(IndividualABC, self).__init__()
        self.pos = []
        self.fit = None
        self.trial = 0

    def copy(self):
        ind = IndividualABC()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)

        ind.paths = copy.deepcopy(self.paths)
        ind.delay = self.delay
        ind.loss = self.loss
        ind.bandwidth = self.bandwidth

        ind.pos = copy.copy(self.pos)
        ind.fit = self.fit
        ind.trial = self.trial
        return ind

    def init_ind(self, problem):
        self.problem = problem
        self.pos = [X_MIN + random.uniform(0,1) * (X_MAX - X_MIN) \
                    for i in range(self.problem.num_link)]

        self.chromosome = self.create_chromosome_by_pos(self.pos)
        self.fitness = self.cal_fitness()

    def create_new_solution(self, ind):
        new_solution = IndividualABC()
        new_solution.problem = self.problem
        new_solution.pos = [x1 + random.uniform(-1,1) * (x1 - x2)  \
                            for x1, x2 in zip(self.pos, ind.pos)]
        new_solution.chromosome = self.create_chromosome_by_pos(new_solution.pos)
        new_solution.fitness = new_solution.cal_fitness()
        return new_solution

    def create_solution_by_generation(self, gen):
        ind = IndividualABC()
        ind.problem = self.problem
        ind.pos = [x + random.uniform(0,1) * (1 - gen / MAX_NUMBER_FUNCTION_EVAL) \
                   for x in self.pos]
        ind.chromosome = self.create_chromosome_by_pos(ind.pos)
        ind.fitness = ind.cal_fitness()
        return ind

    def cal_fit(self, T=None, poplist=None):
        '''

        :param T: temperature, T > 0
        :param poplist: current population
        :return: fitness value
        '''

        # the partition function
        Z = 0.0
        for ind in poplist:
            Z += np.exp(-1.0 * ind.pareto_rank / T)

        # the Gibbs distribution
        Pi = 1.0 * np.exp(-1.0 * self.pareto_rank / T) / Z
        Si = -1.0 * Pi * np.log(Pi)
        fit = self.pareto_rank - T * Si - self.crowding_distance

        return 1.0 / fit

    def create_chromosome_by_pos(self, pos):
        return [1 if random.uniform(0,1) < func(x) else 0 for x in pos]


class NondominatedSortingArtificialBeeColony(MOEA):

    def __init__(self, problem=None):
        super(NondominatedSortingArtificialBeeColony, self).__init__(problem=problem)
        self.limit = POPULATION_SIZE/10

    def name(self):
        return 'NSABC'

    def init_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualABC()
            ind.init_ind(self.problem)
            self.current_population.append(ind)

    def update_archive(self):
        union_set = []
        union_set.extend(self.current_population)
        union_set.extend(self.external_archive)

        first_pareto_rank = fast_nondominated_sort(union_set)[0]
        self.external_archive = []

        if len(first_pareto_rank) > EXTERNAL_ARCHIVE_SIZE:
            crowding_distance_sort(first_pareto_rank)

            while len(first_pareto_rank) > EXTERNAL_ARCHIVE_SIZE:
                first_pareto_rank.pop(-1)

        for ind in first_pareto_rank:
            self.external_archive.append(ind.copy())

    def employee_bee_phase(self, gen=None):
        pop_augment = []

        for index, ind in enumerate(self.current_population):
            select_index = random.randint(0, POPULATION_SIZE-1)
            while select_index == index:
                select_index = random.randint(0, POPULATION_SIZE-1)

            select_ind = self.current_population[select_index]
            solution1 = ind.create_new_solution(select_ind)

            if solution1 <= ind:
                ind = solution1
            else:
                solution2 = ind.create_solution_by_generation(gen)
                if ind <= solution1:
                    pop_augment.append(solution2)
                else:
                    if solution1 <= solution2:
                        pop_augment.append(solution1)
                    else:
                        pop_augment.append(solution2)
                ind.trial += 1

        union_set = []
        union_set.extend(self.current_population)
        union_set.extend(pop_augment)
        self.current_population = make_new_population(union_set, POPULATION_SIZE)

    def onlooker_bee_phase(self):
        fits = []
        for ind in self.current_population:
            fits.append(ind.cal_fit(T=100, poplist=self.current_population))

        p_lst = [x / sum(fits) for x in fits]

        for ind, p in zip(self.current_population, p_lst):
            p_rnd = random.uniform(0,1)
            if p_rnd < p:
                select_index = random.randint(0, POPULATION_SIZE - 1)
                select_ind = self.current_population[select_index]
                while select_ind is ind:
                    select_index = random.randint(0, POPULATION_SIZE - 1)
                    select_ind = self.current_population[select_index]

                new_solution = ind.create_new_solution(select_ind)

                if new_solution <= ind:
                    ind = new_solution
                else:
                    ind.trial += 1

    def scout_bee_phase(self):
        for ind in self.current_population:
            if ind.trial > self.limit:
                ind.init_ind(self.problem)
                ind.trial = 0

    def run(self):
        self.init_population()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            print "Gen = ", gen, ' >>> archive size = ', len(self.external_archive)
            self.employee_bee_phase(gen)
            self.onlooker_bee_phase()
            self.scout_bee_phase()
            self.update_archive()
            gen += 1

        return self.external_archive