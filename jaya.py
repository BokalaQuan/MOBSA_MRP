from algorithm.individual import IndividualMRP
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.operator import *
from algorithm.util import *

import random
import copy
import networkx as nx


class IndividualJaya(IndividualMRP):
    def __init__(self):
        super(IndividualJaya, self).__init__()
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0

        self.position = []

        self.G = None

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

        ind.G = self.G

        return ind

    def init_position(self):
        self.position = np.random.randn(self.problem.num_link)

    def trans_pos_to_chr(self, position):
        chrom = [1 if func_trans_S1(pos) < random.random() else 0 for pos in position]
        return chrom

    def init_ind(self, problem, G):
        self.problem = problem
        self.G = G
        self.init_position()
        self.chromosome = self.trans_pos_to_chr(self.position)
        self.cal_fitness(chromosome=self.chromosome)

    def _init_subgraph_by_chromosome(self):
        link_select = []
        state = True
        graph = nx.Graph()

        for x in range(self.problem.num_link):
            if self.chromosome[x]:
                link_select.append(self.problem.links[x])

        for link in link_select:
            graph.add_edge(link.src, link.dst, delay=link.delay,
                           bandwidth=link.bandwidth, loss=link.loss,
                           phr=self.G[link.src][link.dst]['phr'])

        if state:
            if self.problem.src not in graph.node:
                state = False
            else:
                for dst in self.problem.dst:
                    if dst not in graph.node:
                        state = False

        if state:
            for dst in self.problem.dst:
                if not nx.has_path(G=graph, source=self.problem.src, target=dst):
                    state = False

        if state:
            self._init_tree_by_subgraph(graph)
        else:
            self.delay = float('inf')
            self.loss = float('inf')

        self.fitness = [self.delay, self.loss]

    def _init_tree_by_subgraph(self, graph):
        self.paths = []

        for d in self.problem.dst:
            path = nx.dijkstra_path(G=graph, source=self.problem.src, target=d, weight="phr")
            self.paths.append(path)

            for index in range(len(path) - 1):
                src = path[index]
                dst = path[index + 1]

                self.G[src][dst]['phr'] -= 0.01

        self._cal_fitness(graph)

    def update_ind(self, ind_best, ind_worst):
        b_pos = ind_best
        w_pos = ind_worst

        pos = [i + random.uniform(0,1)*(b-abs(i)) - random.uniform(0,1)*(w-abs(i)) \
               for i, b, w in zip(self.position, b_pos, w_pos)]

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

    def crowding_operator(self, ind):
        if ind.pareto_rank > self.pareto_rank:
            return True
        elif ind.pareto_rank == self.pareto_rank and \
                ind.crowding_distance < self.crowding_distance:
            return True
        else:
            return False

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
        self.G = problem.graph.copy()

    def name(self):
        return 'MOEA-PCG'

    def init_phrMatrix(self):
        for d in self.problem.dst:
            path_loss = nx.dijkstra_path(G=self.G, source=self.problem.src, target=d, weight="loss")
            path_delay = nx.dijkstra_path(G=self.G, source=self.problem.src, target=d, weight="delay")

            for index in range(len(path_loss) - 1):
                src = path_loss[index]
                dst = path_loss[index + 1]

                self.G[src][dst]['phr'] -= 0.01

            for index in range(len(path_delay) - 1):
                src = path_delay[index]
                dst = path_delay[index + 1]

                self.G[src][dst]['phr'] -= 0.01

    def init_population(self):
        for i in range(POPULATION_SIZE):
            ind = IndividualJaya()
            ind.init_ind(problem=self.problem, G=self.G)
            self.current_population.append(ind)

    def copy_current_to_pre(self):
        self.external_archive = []
        for ind in self.current_population:
            self.external_archive.append(ind.copy())

    def make_new_population(self):
        union_poplist = []
        union_poplist.extend(self.current_population)
        union_poplist.extend(self.external_archive)

        self.current_population = make_new_population(union_poplist, POPULATION_SIZE)

    def select_(self):
        best = None
        worst = None

        index1 = 0
        index2 = 0

        while index1 == index2:
            index1 = random.randint(0, POPULATION_SIZE-1)
            index2 = random.randint(0, POPULATION_SIZE-1)

        ind1 = self.external_archive[index1]
        ind2 = self.external_archive[index2]

        if ind1.crowding_operator(ind2):
            best = ind1
            worst = ind2
        else:
            best = ind2
            worst = ind1

        return copy.copy(best.position), copy.copy(worst.position)


    def evolution(self, gen):
        for ind in self.current_population:
            best, worst = self.select_()
            ind.update_ind(ind_best=best, ind_worst=worst)

            if random.random() < gen / MAX_NUMBER_FUNCTION_EVAL:
                ind.levy_flight()

    def show(self):
        logger.info('Jaya initialization is completed. '
                    'Population size is %s, maximum evolution algebra is %s, ',
                    str(POPULATION_SIZE), str(MAX_NUMBER_FUNCTION_EVAL))

    def run(self):
        self.init_phrMatrix()
        self.init_population()
        self.copy_current_to_pre()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            self.make_new_population()
            self.copy_current_to_pre()
            self.evolution(gen)
            gen += 1

        return self.external_archive

