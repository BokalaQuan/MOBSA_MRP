'''
@author Coello, C. A. C, et. al.
@title "Handling multiple objectives with particle swarm optimization."
@date 2004.
'''

from algorithm.individual import IndividualMRP
from algorithm.parameter import *
from algorithm.util import *
from algorithm.operator import *
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA

import random

VELM = [-3.0, 3.0]

class IndividualParticle(IndividualMRP):
    
    def __init__(self):
        super(IndividualParticle, self).__init__()
        self.vel = []
        self.pbest = None
        self.gbest = None
        
        
    def init_ind(self, problem):
        self.problem = problem
        self.cal_fitness()
        self.pbest = self.copy()
        self.vel = [0.0 for x in range(problem.num_link)]

    def update_particle(self, W, gen):
        for i in range(len(self.vel)):
            vel_ = self.vel[i] * W + \
                random.random() * (self.pbest.chromosome[i] - self.chromosome[i]) + \
                random.random() * (self.gbest.chromosome[i] - self.chromosome[i])
            
            if vel_ < VELM[0]: vel_ = VELM[0]
            elif vel_ > VELM[1]: vel_ = VELM[1]

            # if vel_ < VELM[0] or vel_ > VELM[1]: vel_ *= -1
            
            self.vel[i] = vel_
            
            self.chromosome[i] = 0 if random.random() > func_trans_S1(vel_) else 1
        
        pm = 1 - gen / MAX_NUMBER_FUNCTION_EVAL
        if random.random() < pm:
            self.mutation()
        
        self.cal_fitness()
        
    def update_pbest(self):
        if self >= self.pbest:
            return
        elif self.pbest >= self:
            self.pbest = self.copy()
        else:
            if random.random() < 0.5:
                self.pbest = self.copy()
            else:
                return
            
    def update_gbest(self, solution):
        self.gbest = solution
            

class MultiObjectiveParticleSwarmOptimization(MOEA):
    
    def __init__(self, problem):
        super(MultiObjectiveParticleSwarmOptimization, self).__init__(problem)
        self.problem = problem
        self.grid = AdaptiveGrid(int(EXTERNAL_ARCHIVE_SIZE/2))
        
    def name(self):
        return 'MOPSO'
    
    def initialize_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualParticle()
            ind.init_ind(self.problem)
            self.current_population.append(ind)

            self.grid.update_grid(ind)

    def run(self):
        self.initialize_population()
        
        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            # print "Gen >>> ", gen
            for ind in self.current_population:
                ind.update_gbest(self.grid.get_solution())
                ind.update_particle(0.4, gen)
                ind.update_pbest()
                self.grid.update_grid(ind)
            gen += 1

        return self.grid.get_solutions()