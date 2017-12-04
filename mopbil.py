from algorithm.individual import IndividualMRP
from algorithm.parameter import *
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from problem.kp.knapsack_problem import MultiObjectiveKnapsackProblem as MOKP
from algorithm.util import write_list_to_json, write_performance, read_json_as_list, plot_ps
from algorithm.operator import AdaptiveGrid, fast_nondominated_sort


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
            
    def update_vector(self, chromosome):
        for i in range(len(self.vector)):
            tmp = self.vector[i] * (1 - self.learn_rate) + chromosome[i] * self.learn_rate
            if random.random() < PM:
                tmp = tmp * (1 - self.shift) + random.randint(0, 1) * self.shift
            self.vector[i] = tmp
    
    def generate_chromosome(self):
        chromosome = []
        for p in self.vector:
            chromosome.append(1 if random.random() < p else 0)
            
        return chromosome
            
class SubPopulation(object):
    
    def __init__(self, probability_vector):
        self.pv = probability_vector
        self.population = []
        
    def create_sub_population(self, sub_popsize, problem):
        for i in range(sub_popsize):
            chromosome = self.pv.generate_chromosome()
            ind = IndividualMRP()
            ind.initialize(chromosome, problem)
            self.population.append(ind)
    
    def update_sub_population(self, problem):
        for ind in self.population:
            chromosome = []
            for p in self.pv:
                chromosome.append(1 if random.random() < p else 0)
            ind.initialize(chromosome, problem)
            
        
'''
@author Bureerat, Sujin, et al.
@title "Population-Based Incremental Learning for Multiobjective Optimisation."
@date 2007
'''
class PopulationBasedIncrementalLearning(object):
    
    def __init__(self, problem):
        self.problem = problem
        self.sub_populations = []
        self.current_population = []
        self.external_archive = None
        
    def init_population(self):
        for i in range(POPULATION_SIZE / 5):
            pv = ProbabilityVector()
            pv.init(self.problem.num_link)
            sub = SubPopulation(pv)
            sub.create_sub_population(5, self.problem)
            self.sub_populations.append(sub)
            self.current_population.extend(sub.population)

        archive = fast_nondominated_sort(self.current_population)[0]
        self.external_archive = AdaptiveGrid(10)
        self.external_archive.init_grid(archive)
        
    
    def update_archive(self, ind):
        self.external_archive.update_grid(ind)
        
    
    def update_pv_by_mean(self):
        select_number = random.randint(1, len(self.external_archive.archive)-2)
        chromosome_set = []
        
        for i in range(select_number):
            chromosome_set.append(self.external_archive.archive[i])
        
        chromosome_mean = []
        for i in range(len(self.problem.num_link)):
            tmp_sum = 0
            for chrom in chromosome_set:
                tmp_sum += chrom[i]
            chromosome_mean.append(float(tmp_sum) / len(chromosome_set))
            
        for sub in self.sub_populations:
            sub.pv.update_vector(chromosome_mean)
    
    
    def update_pv_by_weight_sum(self):
        ran = random.uniform(0,1)
        weight_vector = [ran, 1-ran]
        fit_list = []
        for ind in self.external_archive.archive:
            fit = ind.fitness[0] * weight_vector[0] + ind.fitness[1] * weight_vector[1]
            fit_list.append(fit)
        
        index_select = fit_list.index(min(fit_list))
        
        for sub in self.sub_populations:
            sub.pv.update_vector(self.external_archive.archive[index_select].chromosome)
    
    def main(self):
        self.init_population()
    
        
    
    
    
'''
@author Jong-Hwan Kim, et al.
@title "Evolutionary Multi-Objective Optimization in Robot Soccer System for Education."
@date 2009
'''
class MultiObjectivePopulationBasedIncrementalLearning(object):
    
    def __init__(self, problem):
        self.problem = problem
        self.current_population = []
        self.external_archive = []
        self.pv_list = []
    
    def init_population(self):
        for i in range(POPULATION_SIZE):
            pv = ProbabilityVector()
            pv.init(self.problem.num_link)
            self.pv_list.append(pv)
            chromosome = pv.generate_chromosome()
            ind = IndividualMRP()
            ind.initialize(chromosome, self.problem)
            self.current_population.append(ind)
            
    def update_archive(self):
        union_set = []
        union_set.extend(self.current_population)
        union_set.extend(self.external_archive)
        
        self.external_archive = []
        self.external_archive.extend(fast_nondominated_sort(union_set)[0])
        
        if len(self.external_archive) > EXTERNAL_ARCHIVE_SIZE:
            neighbor_distance_set = []
            
            for ind in self.external_archive:
                neighbor_distance = []
                for bhd in self.external_archive:
                    neighbor_distance.append(ind.distance_to(bhd))
                
                neighbor_distance.sort()
                neighbor_distance_set.append(neighbor_distance[1])
            
            tmp = copy.copy(neighbor_distance_set)
            tmp.sort()
            
            delete_num = EXTERNAL_ARCHIVE_SIZE - len(self.external_archive)
            for i in range(delete_num):
                self.external_archive.pop(neighbor_distance_set.index(tmp[i]))
            
    def main(self):
        pass
    


