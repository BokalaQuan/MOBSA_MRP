'''
@author K. Deb, et al.
@title "A fast and elitist multiobjective genetic algorithm: NSGA-II".
@date 2002.
'''
from algorithm.individual import IndividualMRP
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.operator import fast_nondominated_sort, crowding_distance_sort

import random
import copy

class IndividualNSGA(IndividualMRP):
    
    def __init__(self):
        super(IndividualNSGA, self).__init__()
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0

    def copy(self):
        ind = IndividualNSGA()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)

        ind.paths = copy.deepcopy(self.paths)
        ind.delay = self.delay
        ind.loss = self.loss
        ind.bandwidth = self.bandwidth

        ind.num_dominated = 0
        ind.dominating_list = []
        ind.pareto_rank = self.pareto_rank
        ind.crowding_distance = self.crowding_distance

        return ind

    def clear_dominated_property(self):
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0


class NondominatedSortGeneticAlgorithm2(MOEA):
    
    def __init__(self, problem):
        super(NondominatedSortGeneticAlgorithm2, self).__init__(problem)

    def name(self):
        return 'NSGA-II'
    
    def init_population(self):
        for i in xrange(POPULATION_SIZE):
            ind = IndividualNSGA()
            ind.init_ind(problem=self.problem)
            self.current_population.append(ind)
        
    def copy_current_to_pre(self):
        self.external_archive = []
        for ind in self.current_population:
            self.external_archive.append(ind.copy())
            
    def make_new_population(self):
        union_poplist = []
        union_poplist.extend(self.current_population)
        union_poplist.extend(self.external_archive)
        
        pareto_rank_set_list = fast_nondominated_sort(union_poplist)
        crowding_distance_sort(pareto_rank_set_list)
        
        self.current_population = []
        for pareto_rank_set in pareto_rank_set_list:
            if len(self.current_population) < POPULATION_SIZE:
                if (len(pareto_rank_set) + len(self.current_population)) <= POPULATION_SIZE:
                    for ind in pareto_rank_set:
                        self.current_population.append(ind.copy())
                else:
                    current = len(self.current_population)
                    for i in range(POPULATION_SIZE - current):
                        self.current_population.append(pareto_rank_set[i].copy())

    def evolution(self):
        self.current_population = []
        for i in range(POPULATION_SIZE):
            x = 0
            y = 0
            while x == y:
                x = random.randint(0, POPULATION_SIZE-1)
                y = random.randint(0, POPULATION_SIZE-1)
                
            ind1 = self.external_archive[x]
            ind2 = self.external_archive[y]
            
            if ind1.pareto_rank < ind2.pareto_rank:
                self.current_population.append(ind1.copy())
            elif ind1.pareto_rank == ind2.pareto_rank and ind1.crowding_distance > ind2.crowding_distance:
                self.current_population.append(ind1.copy())
            else:
                self.current_population.append(ind2.copy())
                
        for i in range(POPULATION_SIZE/2):
            if random.uniform(0, 1) < PC:
                self.current_population[i].crossover(self.current_population[POPULATION_SIZE-i-1])
        
        for ind in self.current_population:
            ind.mutation()
            ind.fitness = ind.cal_fitness()
            
    def run(self):
        self.init_population()
        self.copy_current_to_pre()
        
        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            self.make_new_population()
            self.copy_current_to_pre()
            self.evolution()
            gen += 1
         
        return self.external_archive
