from algorithm.individual import IndividualMRP
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.operator import *
from algorithm.util import *

import random
import copy


class IndividualJaya(IndividualMRP):
    def __init__(self):
        super(IndividualJaya, self).__init__()
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0

        self.position = []

    def copy(self):
        ind = IndividualJaya()
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

        ind.position = copy.copy(self.position)

        return ind

    def init_position(self):
        self.position = np.random.randn(self.problem.num_link)

    def trans_pos_to_chr(self, position):
        chrom = [1 if func_trans_S2(pos) < random.random() else 0 \
                 for pos in position]
        return chrom

    def init_ind(self, problem):
        self.problem = problem
        self.init_position()
        self.chromosome = self.trans_pos_to_chr(self.position)
        self.cal_fitness(chromosome=self.chromosome)

    def update_ind(self, ind_best, ind_worst):
        b_pos = ind_best
        w_pos = ind_worst

        pos = [i + random.uniform(0,1)*(b-abs(i)) - random.uniform(0,1)*(w-abs(i)) \
               for i, b, w in zip(self.position, b_pos, w_pos)]

        # self.position = [p if p < 3 and p > -3 else -1*p for p in pos]
        self.position = []
        for p in pos:
            if p > 3:
                self.position.append(3.0)
            elif p < -3:
                self.position.append(-3.0)
            else:
                self.position.append(p)

        self.chromosome = self.trans_pos_to_chr(self.position)
        self.cal_fitness(chromosome=self.chromosome)

    def levy_flight(self):
        rnd = func_levy(len(self.position), 1.5)
        self.position *= rnd
        self.chromosome = self.trans_pos_to_chr(self.position)
        self.cal_fitness(chromosome=self.chromosome)



    def clear_dominated_property(self):
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0


class Jaya(MOEA):
    def __init__(self, problem):
        super(Jaya, self).__init__(problem)

    def name(self):
        return 'Jaya'

    def init_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualJaya()
            ind.init_ind(problem=self.problem)
            self.current_population.append(ind)

    def update_archive(self):
        union_lst = []
        union_lst.extend(self.current_population)
        union_lst.extend(self.external_archive)

        first_front = fast_nondominated_sort(union_lst)[0]

        self.external_archive = []

        for ind in first_front:
            self.external_archive.append(ind.copy())

    def select(self):
        union_poplist = []
        union_poplist.extend(self.current_population)
        union_poplist.extend(self.external_archive)

        pareto_rank_set_list = fast_nondominated_sort(union_poplist)
        crowding_distance_sort(pareto_rank_set_list)

        best_lst = []
        worst_lst = []

        best = pareto_rank_set_list[0]
        worst = pareto_rank_set_list[len(pareto_rank_set_list)-1]

        for i in range(POPULATION_SIZE):
            best_lst.append(copy.copy(best[random.randint(0, len(best)-1)].position))
            worst_lst.append(copy.copy(worst[random.randint(0, len(worst)-1)].position))

        return best_lst, worst_lst

    def evolution(self):
        best_lst, worst_lst = self.select()

        for ind, best, worst in zip(self.current_population, best_lst, worst_lst):
            ind.update_ind(ind_best=best, ind_worst=worst)


    def show(self):
        logger.info('Jaya initialization is completed. '
                    'Population size is %s, maximum evolution algebra is %s, ',
                    str(POPULATION_SIZE), str(MAX_NUMBER_FUNCTION_EVAL))

    def run(self):
        self.init_population()
        self.update_archive()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            self.evolution()
            self.update_archive()
            gen += 1

        return self.external_archive


if __name__ == '__main__':
    from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
    from algorithm.individual import IndividualMRP

    problem = MRP()
    problem.initialize(path='/Rand_Topo/', filename='Rand1')

    num_Jaya = 0
    num_Origin = 0

    D = [float('inf'), float('inf')]

    for i in range(50):

        ind = IndividualJaya()
        ind.init_ind(problem)

        print("Jaya >>> " ,ind.fitness)

        ind = IndividualMRP()
        ind.init_ind(problem)

        print("Origin >>> ", ind.fitness)