from algorithm.individual import IndividualMRP
from algorithm.parameter import POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL, PC, PM, INF
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from problem.kp.knapsack_problem import MultiObjectiveKnapsackProblem as MOKP
from algorithm.util import write_list_to_json, write_performance, read_json_as_list, plot_ps

import random
import copy
import numpy

class ProbabilityVector(object):
    
    def __init__(self):
        self.vector = []
        self.learn_rate = None
        self.shift = None
        
    def copy(self):
        pv = ProbabilityVector()
        pv.vector = copy.copy(self.vector)
        pv.learn_rate = self.learn_rate
        pv.shift = self.shift
        return pv
    
    # initialize probability is 0.5.
    def init(self, length):
        for i in range(length):
            self.vector.append(0.5)
            
    def update_vector(self, ind):
        for i in range(len(self.vector)):
            tmp = self.vector[i] * (1 - self.learn_rate) + ind.chromosome[i] * self.learn_rate
            if random.random() < PM:
                tmp = tmp * (1 - self.shift) + random.randint(0, 1) * self.shift
            self.vector[i] = tmp
            
            
class SubPopulation(object):
    
    def __init__(self, probability_vector):
        self.pv = probability_vector
        self.population = []
        
    def create_sub_population(self, sub_popsize, problem):
        for i in range(sub_popsize):
            chromosome = []
            for p in self.pv:
                chromosome.append(1 if random.random() < p else 0)
            ind = IndividualMRP()
            ind.initialize(chromosome, problem)
            self.population.append(ind)
    
'''
@author Bureerat, Sujin, et al.
@title "Population-Based Incremental Learning for Multiobjective Optimisation."
@date 2007
'''
class PopulationBasedIncrementalLearning(object):
    
    def __init__(self, problem):
        self.problem = problem
        self.current_population = []
        self.external_archive = []
        
    def init_population(self):
        for i in range(POPULATION_SIZE / 5):
            pv = ProbabilityVector()
            pv.init(self.problem.num_link)
            sub = SubPopulation(pv)
            sub.create_sub_population(5, self.problem)
            self.current_population.extend(sub.population)
    
    
    
    
'''
@author Jong-Hwan Kim, et al.
@title "Evolutionary Multi-Objective Optimization in Robot Soccer System for Education."
@date 2009
'''
class MultiObjectivePopulationBasedIncrementalLearning(object):
    
    def __init__(self):
        pass
    
        