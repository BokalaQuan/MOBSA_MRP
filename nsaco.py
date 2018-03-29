from nsga2 import IndividualNSGA
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.operator import *
from algorithm.util import logger
from mopbil import ProbabilityVector as PV

import random
import copy
import networkx as nx


class Ant(IndividualNSGA):

    def __init__(self, graphs):
        super(Ant, self).__init__()
        self.graphs = graphs
        self.MulFit = 0

    def copy(self):
        ind = Ant(self.graphs)
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

        ind.MulFit = self.MulFit

        return ind

    def _init_tree_by_subgraph(self, graph):
        self.paths = []

        for i, d in enumerate(self.problem.dst):
            path = nx.dijkstra_path(graph, self.problem.src, d, weight="phr")
            self.paths.append(path)

            for index in range(len(path) - 1):
                src = path[index]
                dst = path[index + 1]

                self.graphs[i].get_edge_data(src, dst)['phr'] -= 0.1

        self._cal_fitness(graph)

    def cal_MulFit(self):
        self.MulFit = 1.0 / (2**(self.pareto_rank) + 1/(1+self.crowding_distance))

class SubPopulation(object):

    def __init__(self, pv):
        self.pv = pv
        self.population = []
        self.set_success = [0 for i in range(MAX_NUMBER_FUNCTION_EVAL)]

    def init_sub_population(self, popsize, problem, graphs):
        for i in range(popsize):
            chromosome = self.pv.generate_chromosome()
            ind = Ant(graphs)
            ind.problem = problem
            ind.cal_fitness(chromosome)
            self.population.append(ind)

    def update_population(self):
        for ind in self.population:
            chromosome = self.pv.generate_chromosome()
            ind.cal_fitness(chromosome=chromosome)



class NSACO(MOEA):

    def __init__(self, problem):
        super(NSACO, self).__init__(problem)
        self.graphs = []
        self.sub_collection = []

    def name(self):
        return "NSACO"

    def init_graph(self, dst):
        graph = self.problem.G.copy()
        return graph

    def init_phrMatrix(self):
        for dst in self.problem.dst:
            G = self.init_graph(dst)

            for d in self.problem.dst:
                path_loss = nx.dijkstra_path(G, source=self.problem.src, target=d, weight="loss")
                path_delay = nx.dijkstra_path(G, source=self.problem.src, target=d, weight="delay")

                for index in range(len(path_loss)-1):
                    src = path_loss[index]
                    dst = path_loss[index+1]

                    G.get_edge_data(src, dst)['phr'] -= 0.1

                for index in range(len(path_delay)-1):
                    src = path_delay[index]
                    dst = path_delay[index + 1]

                    G.get_edge_data(src, dst)['phr'] -= 0.1

            self.graphs.append(G)

    def init_population(self):
        for i in range(5):
            pv = PV(learn_rate=0.5, shift=0.02)
            pv.init_pv(self.problem.num_link)
            sub = SubPopulation(pv)
            sub.init_sub_population(popsize=10, problem=self.problem, graphs=self.graphs)
            self.sub_collection.append(sub)
            self.current_population.extend(sub.population)

            for ind in sub.population:
                self.update_archive(ind)

    '''
    def copy_current_to_pre(self):
        self.external_archive = []
        for ind in self.current_population:
            self.external_archive.append(ind.copy())
    
    def update_archive(self, gen):
        union_poplst = []
        union_poplst.extend(self.current_population)
        union_poplst.extend(self.external_archive)

        pareto_rank_set_list = fast_nondominated_sort(union_poplst)
        crowding_distance_sort(pareto_rank_set_list)

        for ind in union_poplst:
            ind.cal_MulFit()

        union_poplst.sort(key=lambda x: x.MulFit, reverse=True)
        better_poplst = union_poplst[:EXTERNAL_ARCHIVE_SIZE]

        # for sub in self.sub_collection:
        #     for ind in sub.population:
        #         if ind in better_poplst:
        #             sub.set_success[gen] += 1

        self.external_archive = []
        for ind in better_poplst:
            self.external_archive.append(ind.copy())

        # for ind in union_poplst[EXTERNAL_ARCHIVE_SIZE:]:
        #     self.update_phrMatrix(ind)
    '''

    def update_archive(self, ind):
        if len(self.external_archive) == 0:
            self.external_archive.append(ind.copy())
        else:
            flag = False
            for item in self.external_archive:
                if item <= ind or item == ind:
                    flag = True
                    break
                elif item >= ind:
                    del(item)

            if not flag:
                self.external_archive.append(ind.copy())

    def update_phrMatrix(self, ind):
        for graph, path in zip(self.graphs, ind.paths):
            for index in range(len(path)-1):
                src = path[index]
                dst = path[index+1]

                graph.get_edge_data(src, dst)['phr'] += 0.1

    def select_better_solution(self):
        length = len(self.external_archive)

        index1, index2 = 0, 0
        while index1 == index2:
            index1, index2 = random.randint(0, length-1), random.randint(0, length-1)

        ind1 = self.external_archive[index1]
        ind2 = self.external_archive[index2]

        if ind1 <= ind2:
            return ind1
        elif ind2 <= ind1:
            return ind2
        else:
            return ind1 if random.random() < 0.5 else ind2

    def evolution(self):
        for sub in self.sub_collection:
            ref = self.select_better_solution()
            sub.pv.update_vector(ref.chromosome)
            sub.update_population()

            for ind in sub.population:
                self.update_archive(ind)

    def show(self):
        logger.info('NSACO initialization is completed. '
                    'Population size is %s, maximum evolution algebra is %s, neighbors size is %s, '
                    'decomposition way is %s, cross probability is %s, mutation probability is %s.',
                    str(POPULATION_SIZE), str(MAX_NUMBER_FUNCTION_EVAL), str(NUMBER_NEIGHBOR),
                    str('Weight-sum'), str(PC), str(PM))

    def run(self):
        self.init_phrMatrix()
        self.init_population()

        gen = 0
        while gen < 100:
            logger.info("Gen >>> %s", str(gen))
            self.evolution()

            gen += 1

        return self.external_archive

