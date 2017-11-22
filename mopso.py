'''
Coello, C. A. C, et. al.
"Handling multiple objectives with particle swarm optimization."
IEEE Transactions on Evolutionary Computation 8.3(2004):256-279.
'''

from algorithm.individual import IndividualMRP
from algorithm.parameter import PM, PC, POPULATION_SIZE, EXTERNAL_ARCHIVE_SIZE, MAX_NUMBER_FUNCTION_EVAL
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from algorithm.util import func_trans_V1, func_trans_S1, write_list_to_json, read_json_as_list, write_performance
from algorithm.operator import fast_nondominated_sort
from algorithm.performance import cal_HV, cal_GD, cal_IGD

import numpy
import random
import copy
import os
import json

import matplotlib.pyplot as plot

VELM = [-2, 2]
INF = float('inf')

class IndividualParticle(IndividualMRP):
    
    def __init__(self):
        super(IndividualParticle, self).__init__()
        self.vel = []
        self.num_grid = []
        self.pbest = None
        self.gbest = None
        
        
    def initialize(self, chromosome, problem):
        self.chromosome = chromosome
        self.problem = problem
        self.pbest = self.copy()
        self.vel = [0.0 for x in range(len(chromosome))]
        self.fitness = self.cal_fitness()
        
    def update_particle(self, W, gen):
        for i in range(len(self.vel)):
            vel_ = self.vel[i] * W + \
                random.random() * (self.pbest.chromosome[i] - self.chromosome[i]) + \
                random.random() * (self.gbest.chromosome[i] - self.chromosome[i])
            
            if vel_ < VELM[0]: vel_ = VELM[0]
            elif vel_ > VELM[1]: vel_ = VELM[1]
            
            self.vel[i] = vel_
            
            self.chromosome[i] = 0 if random.random() > func_trans_S1(vel_) else 1
        
        pm = 1 - gen / MAX_NUMBER_FUNCTION_EVAL
        if random.random() < pm:
            self.mutation()
        
        self.fitness = self.cal_fitness()
        
    def update_pbest(self):
        if self.is_dominated(self.pbest):
            return
        elif self.pbest.is_dominated(self):
            self.pbest = self.copy()
        else:
            if random.random() < 0.5:
                self.pbest = self.copy()
            else:
                return
            
    def update_gbest_by_randomly(self, poplist):
        ran = random.randint(0, len(poplist) - 1)
        self.gbest = poplist[ran].copy()
    
    def update_gbest_by_hypercube(self, hypercubes):
        if len(hypercubes) == 1:
            self.gbest = hypercubes[0][random.randint(0, len(hypercubes[0]) - 1)].copy()
        else:
            select_probability = []
            for cube in hypercubes:
                select_probability.append(10.0 / len(cube))
            temp = sum(select_probability)
            for i in range(len(select_probability)):
                select_probability[i] /= temp
                
            for i in range(len(select_probability)):
                temp += select_probability[i]
                select_probability[i] = temp
                
            ran = random.random()
            index = 0
            if ran < select_probability[0]:
                index = 0
            else:
                for i in range(1, len(select_probability)):
                    if ran < select_probability[i] and \
                        ran >= select_probability[i-1]:
                        index = i
            
            self.gbest = hypercubes[index][random.randint(0, len(hypercubes[index]) - 1)].copy()
            

def adaptive_grid_archive(poplist, gridsize):
    hypercubes = []
    upper = [0.0, 0.0]
    lower = [INF, INF]
    
    for ind in poplist:
        upper[0] = ind.fitness[0] if ind.fitness[0] > upper[0] else upper[0]
        upper[1] = ind.fitness[1] if ind.fitness[1] > upper[1] else upper[1]
        lower[0] = ind.fitness[0] if ind.fitness[0] < lower[0] else lower[0]
        lower[1] = ind.fitness[1] if ind.fitness[1] < lower[1] else lower[1]
    
    mod = [(upper[0] - lower[0]) / gridsize, (upper[1] - lower[1]) / gridsize]

    for ind in poplist:
        ind.num_grid = [int((ind.fitness[0] - lower[0]) / mod[0]),
                        int((ind.fitness[1] - lower[1]) / mod[1])]
    
    for i in range(gridsize):
        for j in range(gridsize):
            hypercube = []
            for ind in poplist:
                if ind.num_grid == [i, j]: hypercube.append(ind)
            if len(hypercube) != 0: hypercubes.append(hypercube)
    
    return hypercubes

class MultiObjectiveParticleSwarmOptimization(object):
    
    def __init__(self, problem):
        self.problem = problem
        self.current_population = []
        self.external_population = []
        
    def initialize_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualParticle()
            ind.initialize(IndividualMRP.create_chromosome(self.problem.num_link), self.problem)
            self.current_population.append(ind)
            self.update_external_population(ind)

    def update_external_population(self, ind):
        if self.external_population is None or len(self.external_population) == 0:
            self.external_population.append(ind.copy())
        else:
            flag = 0
            for exter in self.external_population[:]:
                if exter.is_dominated(ind):
                    self.external_population.remove(exter)
                elif ind.is_dominated(exter) or exter.is_same(ind):
                    flag += 1
                    
            if flag == 0: self.external_population.append(ind.copy())
            
    
    def main(self):
        self.initialize_population()
        
        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            # print "Gen >>> ", gen
            for ind in self.current_population:
                # ind.update_gbest_by_hypercube(adaptive_grid_archive(self.external_population, 2))
                ind.update_gbest_by_randomly(self.external_population)
                ind.update_particle(0.4, gen)
                ind.update_pbest()
                self.update_external_population(ind)
            gen += 1
            

if __name__ == '__main__':
    topo = 'topo5'
    problem = MRP()
    problem.initialize(topo)
    
    # print problem.src
    # print problem.dst
    
    
    pideal = read_json_as_list(topo, 'ideal')
    x = pideal[0]['delay'] + (pideal[0]['delay'] - pideal[len(pideal) - 1]['delay']) * 0.1
    y = pideal[len(pideal) - 1]['loss'] + (pideal[len(pideal) - 1]['loss'] - pideal[0]['loss']) * 0.1
    ref = [x, y]

    IGD = []
    GD = []
    HV = []
    for i in range(10):
        print 'Runtime >>> ', i+1
        test = MultiObjectiveParticleSwarmOptimization(problem)
        test.main()
        write_list_to_json(topo, 'mopso', test.external_population)

        preal = read_json_as_list(topo, 'mopso')

        IGD.append(cal_IGD(pideal, preal))
        GD.append(cal_GD(pideal, preal))
        HV.append(cal_HV(preal, ref))

    per = {'IGD':IGD,
           'GD': GD,
           'HV': HV}

    write_performance('performance', topo, 'mopso', per)