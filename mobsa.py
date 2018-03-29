"""
@author  Xiangyuan Jiang, Shuai Li.
@title "BAS: Beetle Antennae Search Algorithm for Optimization Problems."
@date 2017
"""

from algorithm.individual import IndividualMRP
from algorithm.parameter import POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from algorithm.util import *
from algorithm.operator import fast_nondominated_sort

import numpy
import random
import time

POS_E = [-3, 3]

class IndividualBeetle(IndividualMRP):

    def __init__(self):
        super(IndividualBeetle, self).__init__()
        self.position = []
        # antennae length
        self.alpha = 0.5
        # step size
        self.beta = 2.0

        self.left_lst = [[], []]
        self.right_lst = [[], []]
        self.current_lst = [[], []]


    def init_position(self):
        self.position = np.random.randn(self.problem.num_link)

    def trans_pos_to_chr(self, position):
        chrom = [1 if func_trans_S1(pos) < random.uniform(0, 1) else 0 \
                 for pos in position]
        return chrom

    def init_ind(self, problem):
        self.problem = problem
        self.init_position()
        self.chromosome = self.trans_pos_to_chr(self.position)
        self.cal_fitness(chromosome=self.chromosome)

    def generate_direction_vector(self):
        direct = numpy.random.rand(self.problem.num_link)
        # temp = numpy.linalg.norm(direct)
        # direct /= temp
        return direct

    def update_position(self, direct):
        xleft = []
        xright = []

        for pi, di in zip(self.position, direct):
            xleft.append(pi - self.beta * di)
            xright.append(pi + self.beta * di)

        cleft = self.trans_pos_to_chr(xleft)
        cright = self.trans_pos_to_chr(xright)

        ind_left = IndividualMRP()
        ind_right = IndividualMRP()

        ind_left.problem = self.problem
        ind_right.problem = self.problem

        ind_left.cal_fitness(chromosome=cleft)
        ind_right.cal_fitness(chromosome=cright)

        if ind_left <= ind_right:
            tmp = [pi - self.alpha * di for pi, di in zip(self.position, direct)]
            pos = [x if x < POS_E[1] and x > POS_E[0] else -1 * x for x in tmp]

        elif ind_left >= ind_right:
            tmp = [pi + self.alpha * di for pi, di in zip(self.position, direct)]
            pos = [x if x < POS_E[1] and x > POS_E[0] else -1 * x for x in tmp]
        else:
            flag = 1 if random.uniform(0, 1) < 0.5 else -1
            pos = [pi + flag * self.alpha * di for pi, di in zip(self.position, direct)]

        self.position = pos
        self.chromosome = self.trans_pos_to_chr(self.position)
        self.cal_fitness(chromosome=self.chromosome)

        self.left_lst[0].append(ind_left.fitness[0])
        self.left_lst[1].append(ind_left.fitness[1])
        self.right_lst[0].append(ind_right.fitness[0])
        self.right_lst[1].append(ind_right.fitness[1])
        self.current_lst[0].append(self.fitness[0])
        self.current_lst[1].append(self.fitness[1])


    # def update_position(self, direct):
    #     xleft = []
    #     xright = []
    #
    #     for bi, di in zip(self.position, direct):
    #         xleft.append(1 if random.random() <= func_trans_V1(bi - self.beta * di) else 0)
    #         xright.append(1 if random.random() <= func_trans_V1(bi + self.beta * di) else 0)
    #
    #     ind_left = IndividualMRP()
    #     ind_right = IndividualMRP()
    #
    #     ind_left.problem = self.problem
    #     ind_right.problem = self.problem
    #
    #     ind_left.cal_fitness(chromosome=xleft)
    #     ind_right.cal_fitness(chromosome=xright)
    #
    #     chrom = []
    #     if ind_left >= ind_right:
    #         for bi, di in zip(self.position, direct):
    #             chrom.append(1 if random.random() <= func_trans_V1(bi + self.alpha * di) else 0)
    #             self.chromosome = chrom
    #     elif ind_right >= ind_left:
    #         for bi, di in zip(self.position, direct):
    #             chrom.append(1 if random.random() <= func_trans_V1(bi - self.alpha * di) else 0)
    #             self.chromosome = chrom
    #     elif ind_left != ind_right:
    #         if random.random() < 0.5:
    #             for bi, di in zip(self.position, direct):
    #                 chrom.append(1 if random.random() <= func_trans_V1(bi + self.alpha * di) else 0)
    #                 self.chromosome = chrom
    #         else:
    #             for bi, di in zip(self.chromosome, direct):
    #                 chrom.append(1 if random.random() <= func_trans_V1(bi - self.alpha * di) else 0)
    #                 self.chromosome = chrom
    #     else:
    #         self.mutation()
    #
    #
    #     self.cal_fitness()
    #
    #     print("left: "+str(ind_left.fitness))
    #     print("right: " + str(ind_right.fitness))
    #     print(self.fitness)

    def update_parameters(self, gen):
        # self.alpha = (0.9 - 0.1) * gen / MAX_NUMBER_FUNCTION_EVAL + 0.1
        # self.beta = (0.1 - 0.9) * gen / MAX_NUMBER_FUNCTION_EVAL + 0.9

        self.alpha = 0.95 * self.alpha
        self.beta = 0.95 * self.beta + 0.01

    def update_beetle(self, gen):
        # print "Since update >>> ", self.fitness
        direct = self.generate_direction_vector()
        self.update_position(direct)
        self.update_parameters(gen)
        # print "After update >>> ", self.fitness


class MultiObjectiveBeetleSearchAlgorithm(object):

    def __init__(self, problem):
        self.problem = problem
        self.current_population = []
        self.external_population = []
    
    def name(self):
        return 'MOBSO'

    def init_population(self):
        # Initialize current population and external population
        for i in range(POPULATION_SIZE):
            ind = IndividualBeetle()
            # position = numpy.random.rand(self.problem.num_link)
            ind.init_ind(self.problem)
            self.current_population.append(ind)
            # self.update_external_population(ind)

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


    def run(self):
        self.init_population()

        gen = 0
        while gen < 100:
            print("Gen >>> ", gen)
            for ind in self.current_population:
                ind.update_beetle(gen)
                # self.update_external_population(ind)
            gen += 1

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    path = '/Rand_Topo/'
    topo = 'Rand1'

    problem = MRP()
    problem.initialize(path=path, filename=topo)

    test = MultiObjectiveBeetleSearchAlgorithm(problem)

    test.run()

    ind = test.current_population[0]

    plt.figure()
    for i in range(MAX_NUMBER_FUNCTION_EVAL):
        plt.scatter(ind.current_lst[0][i], ind.current_lst[1][i], s=15.0 * (i+1), alpha=0.5)

    plt.show()


    # plt.scatter(test.current_population[0].left_lst[0], test.current_population[0].left_lst[1])
    # plt.scatter(test.current_population[0].right_lst[0], test.current_population[0].right_lst[1])
    # plt.scatter(test.current_population[0].current_lst[0], test.current_population[0].current_lst[1])

    # plt.show()
