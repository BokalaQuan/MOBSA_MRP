from nsga2 import IndividualNSGA
from algorithm.moea import MultiObjectiveEvolutionaryAlgorithm as MOEA
from algorithm.parameter import *
from algorithm.operator import *
from algorithm.util import logger

import random
import copy
import networkx as nx

class IndividualBeetle(IndividualNSGA):

    def __init__(self, graphs):
        super(IndividualBeetle, self).__init__()
        self.graphs = graphs
        self.pos = np.random.randn(self.problem.num_link)

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



class NondominatedSortBeetleSearchOptimization(MOEA):

    def __init__(self, problem):
        super(NondominatedSortBeetleSearchOptimization, self).__init__(problem)
        self.graphs = []


    def name(self):
        return "NondominatedSortBeetleSearchOptimization"

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

