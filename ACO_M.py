from algorithm.individual import IndividualMRP
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.operator import fast_nondominated_sort, crowding_distance_sort
from nsga2 import *

import random
import copy
import networkx as nx

class Ant(IndividualNSGA):

    def __init__(self, graphs):
        super(Ant, self).__init__()
        self.graphs = graphs

    def _init_tree_by_subgraph(self, graph):
        self.paths = []

        for i, d in enumerate(self.problem.dst):
            path = nx.dijkstra_path(graph, self.problem.src, d, weight="phr")
            self.paths.append(path)

            for index in range(len(path) - 1):
                src = path[index]
                dst = path[index + 1]

                self.graphs[i].get_edge_data(src, dst)['phr'] -= 0.2

        self._cal_fitness(graph)

class ACO(MOEA):

    def __init__(self, problem):
        super(ACO, self).__init__(problem=problem)
        self.graphs = []

    def name(self):
        return "ACO"

    def init_graph(self, dst):
        graph = nx.Graph()
        for link in self.problem.links:
            graph.add_edge(link.src, link.dst, delay=link.delay, loss=link.loss, phr=100.0)
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

                    G.get_edge_data(src, dst)['phr'] -= 0.2

                for index in range(len(path_delay) - 1):
                    src = path_delay[index]
                    dst = path_delay[index + 1]

                    G.get_edge_data(src, dst)['phr'] -= 0.2

            self.graphs.append(G)

    def init_population(self):
        for i in range(POPULATION_SIZE):
            ind = Ant(self.graphs)
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
                x = random.randint(0, POPULATION_SIZE - 1)
                y = random.randint(0, POPULATION_SIZE - 1)

            ind1 = self.external_archive[x]
            ind2 = self.external_archive[y]

            if ind1.pareto_rank < ind2.pareto_rank:
                self.current_population.append(ind1.copy())
            elif ind1.pareto_rank == ind2.pareto_rank and ind1.crowding_distance > ind2.crowding_distance:
                self.current_population.append(ind1.copy())
            else:
                self.current_population.append(ind2.copy())

        for i in range(POPULATION_SIZE / 2):
            if random.uniform(0, 1) < PC:
                self.current_population[i].crossover(self.current_population[POPULATION_SIZE - i - 1])

        for ind in self.current_population:
            ind.mutation()
            ind.fitness = ind.cal_fitness()

    def run(self):
        self.init_phrMatrix()
        self.init_population()
        self.copy_current_to_pre()

        gen = 0
        while gen < MAX_NUMBER_FUNCTION_EVAL:
            self.make_new_population()
            self.copy_current_to_pre()
            self.evolution()
            gen += 1

        return self.external_archive



