"""
@author  Xiangyuan Jiang, Shuai Li.
@title "BAS: Beetle Antennae Search Algorithm for Optimization Problems."
@date 2017
"""

from algorithm.individual import IndividualMRP
from algorithm.parameter import POPULATION_SIZE, MAX_NUMBER_FUNCTION_EVAL
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from algorithm.util import func_trans_S1, write_list_to_json, read_json_as_list, write_performance, func_trans_S2, func_trans_V1
from algorithm.operator import fast_nondominated_sort
from algorithm.performance import cal_GD, cal_HV, cal_IGD

import numpy
import random
import time

class IndividualBeetle(IndividualMRP):

    def __init__(self):
        super(IndividualBeetle, self).__init__()
        # self.position = []
        # antennae length
        self.alpha = 0
        # step size
        self.beta = 0

    def generate_direction_vector(self):
        direct = numpy.random.rand(self.problem.num_link)
        # temp = numpy.linalg.norm(direct)
        # direct /= temp
        return direct

    def update_position(self, direct):
        xleft = []
        xright = []

        for bi, di in zip(self.chromosome, direct):
            xleft.append(1 if random.random() <= func_trans_S1(bi - self.beta * di) else 0)
            xright.append(1 if random.random() <= func_trans_S1(bi + self.beta * di) else 0)

        ind_left = IndividualMRP()
        ind_right = IndividualMRP()
        ind_left.initialize(xleft, self.problem)
        ind_right.initialize(xright, self.problem)
        chrom = []
        if ind_left.is_dominated(ind_right):
            for bi, di in zip(self.chromosome, direct):
                chrom.append(1 if random.random() <= func_trans_S1(bi + self.alpha * di) else 0)
                self.chromosome = chrom
        elif ind_right.is_dominated(ind_left):
            for bi, di in zip(self.chromosome, direct):
                chrom.append(1 if random.random() <= func_trans_S1(bi - self.alpha * di) else 0)
                self.chromosome = chrom
        elif ind_left.fitness != ind_right.fitness:
            if random.random() < 0.5:
                for bi, di in zip(self.chromosome, direct):
                    chrom.append(1 if random.random() <= func_trans_S1(bi + self.alpha * di) else 0)
                    self.chromosome = chrom
            else:
                for bi, di in zip(self.chromosome, direct):
                    chrom.append(1 if random.random() <= func_trans_S1(bi - self.alpha * di) else 0)
                    self.chromosome = chrom
        else:
            self.mutation()


        self.fitness = self.cal_fitness()

    def update_parameters(self, gen):
        self.alpha = (0.9 - 0.1) * gen / MAX_NUMBER_FUNCTION_EVAL + 0.1
        self.beta = (0.1 - 0.9) * gen / MAX_NUMBER_FUNCTION_EVAL + 0.9

    def update_beetle(self, gen):
        # print "Since update >>> ", self.fitness
        self.update_parameters(gen)
        direct = self.generate_direction_vector()
        self.update_position(direct)
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


    def run(self):
        self.init_population()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            # print "Gen >>> ", gen
            for ind in self.current_population:
                ind.update_beetle(gen)
                self.update_external_population(ind)
            gen += 1


if __name__ == '__main__':
    # topo = 'topo1'
    # problem = MRP()
    # problem.initialize(topo)
    #
    # # pf_list = []
    # pideal = read_json_as_list(topo, 'ideal')
    # x = pideal[0]['delay'] + (pideal[0]['delay'] - pideal[len(pideal) - 1]['delay']) * 0.1
    # y = pideal[len(pideal) - 1]['loss'] + (pideal[len(pideal) - 1]['loss'] - pideal[0]['loss']) * 0.1
    # ref = [x, y]
    #
    # IGD = []
    # GD = []
    # HV = []
    # for i in range(10):
    #
    #     begin = time.time()
    #     test = MultiObjectiveBeetleSearchAlgorithm(problem)
    #     test.main()
    #     end = time.time()
    #     print '>>>>>> ', i + 1, '  Runtime = ', int(end - begin)
    #
    #     write_list_to_json(topo, 'mobas', test.external_population)
    #
    #     preal = read_json_as_list(topo, 'mobas')
    #
    #     IGD.append(cal_IGD(pideal, preal))
    #     GD.append(cal_GD(pideal, preal))
    #     HV.append(cal_HV(preal, ref))
    #
    # per = {'IGD': IGD,
    #        'GD': GD,
    #        'HV': HV}
    #
    # print 'IGD >>> ', round(numpy.array(IGD).mean(),2), round(numpy.array(IGD).min(),2), round(numpy.array(IGD).std(), 2)
    # print 'GD >>> ', round(numpy.array(GD).mean(),2), round(numpy.array(GD).min(),2), round(numpy.array(GD).std(), 2)
    # print 'HV >>> ', round(numpy.array(HV).mean(),2), round(numpy.array(HV).min(),2), round(numpy.array(HV).std(), 2)
    #
    # write_performance('performance', topo, 'mobas', per)
    #
    topo = ['topo2', 'topo6']

    for item in topo:
        print "Topo init", item
        problem = MRP()
        problem.initialize(item)

        pf_list = []

        for i in range(10):
            print "Runtime >>> ", i + 1
            test = MultiObjectiveBeetleSearchAlgorithm(problem)
            test.main()
            pf_list.extend(test.external_population)

        pf_ = fast_nondominated_sort(pf_list)[0]
        for i in range(0, len(pf_)):
            for j in range(len(pf_) - 1, i + 1, -1):
                if pf_[i].is_equal(pf_[j]):
                    pf_.pop(j)

        write_list_to_json(item, 'mobso', pf_)

