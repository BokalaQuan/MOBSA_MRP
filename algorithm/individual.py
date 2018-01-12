from parameter import *

import random
import copy
import numpy
import networkx as nx


class Individual(object):
    """
    The class for Multi-objective optimization's individual.
    It represent into a Bi-objective optimization problem.
    """

    def __init__(self):
        self.problem = None
        self.chromosome = None
        self.fitness = None

    def __lt__(self, other):
        for i, j in zip(self.fitness, other.fitness):
            if i >= j:
                return False
        return True

    def __gt__(self, other):
        for i, j in zip(self.fitness, other.fitness):
            if i <= j:
                return False
        return True

    def __eq__(self, other):
        if self.fitness == other.fitness:
            return True
        return False

    def __ne__(self, other):
        if self.fitness != other.fitness:
            return True
        return False

    def __le__(self, other):
        for i, j in zip(self.fitness, other.fitness):
            if i > j:
                return False
        if self.fitness == other.fitness:
            return False
        return True

    def __ge__(self, other):
        for i, j in zip(self.fitness, other.fitness):
            if i < j:
                return False
        if self.fitness == other.fitness:
            return False
        return True

    def __str__(self):
        return "id = " + str(id(self)) + ", Fitness = " + str(self.fitness)

    def copy(self):
        pass

    def init_ind(self):
        pass

    def cal_fitness(self):
        pass

    def distance_to(self, ind):
        fit1 = numpy.array(self.fitness)
        fit2 = numpy.array(ind.fitness)

        return numpy.linalg.norm(fit1 - fit2)

    def to_dict(self):
        return {'fit': self.fitness}

    @staticmethod
    def create_chromosome(length, probability):
        return [1 if random.uniform(0, 1) < probability else 0 for i in range(length)]

class IndividualMRP(Individual):

    def __init__(self):
        super(IndividualMRP, self).__init__()
        self.paths = []

        self.delay = 0.0
        self.loss = 0.0
        self.bandwidth = INF

    def copy(self):
        ind = IndividualMRP()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)

        ind.paths = copy.deepcopy(self.paths)
        ind.delay = self.delay
        ind.loss = self.loss
        ind.bandwidth = self.bandwidth
        return ind

    def init_ind(self, problem):
        """

        :param problem: input problem
        """
        self.problem = problem
        self.chromosome = Individual.create_chromosome(problem.num_link, P_INIT)
        self.fitness = self.cal_fitness()

    def cal_fitness(self):
        self._init_subgraph_by_chromosome(self.problem)
        return [self.delay, self.loss]

    def _init_subgraph_by_chromosome(self, mrp):
        link_select = []
        state = True
        graph = nx.Graph()

        for x in range(mrp.num_link):
            if self.chromosome[x]:
                link_select.append(mrp.links[x])

        for link in link_select:
            graph.add_edge(link.src, link.dst, delay=link.delay,
                           band=link.bandwidth, loss=link.loss)

        if state:
            if mrp.src not in graph.node:
                state = False
            else:
                for dst in mrp.dst:
                    if dst not in graph.node:
                        state = False

        if state:
            for dst in mrp.dst:
                if not nx.has_path(G=graph, source=mrp.src, target=dst):
                    state = False

        if state:
            self._init_tree_by_subgraph(self.problem, graph)
        else:
            self.delay = float(800)
            self.loss = float(1)

    def _init_tree_by_subgraph(self, mrp, graph):
        self.paths = []
        weight = 'delay' if random.random() <= 0.5 else 'loss'
        for dst in mrp.dst:
            path = nx.dijkstra_path(graph, mrp.src, dst, weight=weight)
            self.paths.append(path)

        self._cal_fitness(mrp, graph)

    def _cal_fitness(self, mrp, graph):
        max_delay = 0.0
        max_loss = 0.0

        for path in self.paths:
            delay = 0.0
            loss = 1.0
            for index in range(len(path) - 1):
                delay += graph.edges[path[index], path[index + 1]]['delay']
                loss *= 1 - graph.edges[path[index], path[index + 1]]['loss']
                if self.bandwidth > graph.edges[path[index], path[index + 1]]['band']:
                    self.bandwidth = graph.edges[path[index], path[index + 1]]['band']

            max_delay += delay
            max_loss += 1 - loss

        self.delay = float(max_delay / len(mrp.dst))
        self.loss = float(max_loss / len(mrp.dst))

    def is_feasible(self):
        if self.fitness != [float(800), float(1)]:
            return True
        return False

    def crossover(self, ind):
        """
        @function Uniform crossover
        :param ind:
        :return:
        """
        temp = self.create_chromosome(self.problem.num_link, 0.5)
        for i in range(len(temp)):
            if temp[i]:
                obj = self.chromosome[i]
                self.chromosome[i] = ind.chromosome[i]
                ind.chromosome[i] = obj

    def mutation(self):
        for i in range(len(self.chromosome)):
            self.chromosome[i] = 1 - self.chromosome[i] \
                if random.random() < PM else self.chromosome[i]

    def mutation_1(self):
        tmp = [1 if random.uniform(0, 1) < PM else 0 \
               for i in range(len(self.chromosome))]

        for i, j in enumerate(tmp):
            if j:
                ch = self.chromosome[i]
                if i == 0:
                    self.chromosome[i] = self.chromosome[i + 1]
                    self.chromosome[i + 1] = ch
                else:
                    self.chromosome[i] = self.chromosome[i - 1]
                    self.chromosome[i - 1] = ch

    def opposition_based_learning(self):
        chrom = [1 if ch == 0 else 0 for ch in self.chromosome]
        ind = IndividualMRP()
        ind.problem = self.problem
        ind.chromosome = chrom
        ind.fitness = ind.cal_fitness()
        return ind

    # def to_dict(self):
    #     return {
    #         'delay': self.delay,
    #         'loss': self.loss,
    #         'bandwidth': self.bandwidth,
    #         'paths': str(self.paths)
    #     }


class IndividualKP(Individual):
    def __init__(self):
        super(IndividualKP, self).__init__()

    def copy(self):
        ind = IndividualKP()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)
        return ind

    def init_ind(self, problem):
        self.problem = problem
        self.chromosome = Individual.create_chromosome(problem.num_item, P_INIT)
        self.fitness = self.cal_fitness()

    def cal_fitness(self):
        profits = []
        weights = []
        ratios = []

        for x in range(2):
            profit = []
            weight = []
            ratio = []
            for y in range(len(self.chromosome)):
                if self.chromosome[y]:
                    profit.append(self.problem[x]['items'][y]['profit'])
                    weight.append(self.problem[x]['items'][y]['weight'])
                    ratio.append(self.problem[x]['items'][y]['ratio'])

            profits.append(profit)
            weights.append(weight)
            ratios.append(ratio)

        capacity = [self.problem[0]['capacity'], self.problem[1]['capacity']]
        self.greedy_repair_heuristic(profits, weights, ratios, capacity, self.chromosome)
        return [sum(profits[0]), sum(profits[1])]

    def greedy_repair_heuristic(self, profits, weights, ratios, capacity, chromosome):
        for weight, profit, ratio, cap in zip(weights, profits, ratios, capacity):
            weight_sum = sum(weight)
            while weight_sum > cap:
                min_ratio = min(ratio)
                id_delete = ratio.index(min_ratio)
                chromosome[id_delete] = 0
                profit.pop(id_delete)
                weight.pop(id_delete)
                ratio.pop(id_delete)
                weight_sum = sum(weight)

    def crossover(self, ind):
        temp = self.create_chromosome(self.problem.num_item, 0.5)
        for i in range(len(temp)):
            if temp[i]:
                obj = self.chromosome[i]
                self.chromosome[i] = ind.chromosome[i]
                ind.chromosome[i] = obj

    def mutation(self):
        for i in range(len(self.chromosome)):
            self.chromosome[i] = 1 - self.chromosome[i] \
                if random.random() < PM else self.chromosome[i]

    def opposition_based_learning(self):
        chrom = [1 if ch == 0 else 0 for ch in self.chromosome]
        ind = IndividualKP()
        ind.problem = self.problem
        ind.chromosome = chrom
        ind.fitness = ind.cal_fitness()
        return ind
