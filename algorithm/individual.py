from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from problem.kp.knapsack_problem import MultiObjectiveKnapsackProblem as MOKP
from parameter import INF, PM, PC

import random
import copy
import numpy
import networkx as nx

class Individual(object):
    '''
    '''
    problem = None
    chromosome = []
    fitness = None

    #
    num_dominated = 0
    dominating_list = []
    pareto_rank = 0
    crowding_distance = 0
    
    def __init__(self):
        self.problem = None
        self.chromosome = None
        self.fitness = None
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0
    
    def copy(self):
        pass
    
    def initialize(self, chromosome, problem):
        pass
    
    def cal_fitness(self):
        pass
        
    def is_dominated(self, ind):
        pass
    
    def is_equal(self, ind):
        if self.fitness == ind.fitness:
            return True
        else:
            return False
    
    def is_same(self, ind):
        if self.chromosome == ind.chromosome:
            return True
        else:
            return False
        
    def clear_dominated_property(self):
        self.num_dominated = 0
        self.dominating_list = []
        self.pareto_rank = 0
        self.crowding_distance = 0
    
    def distance_to(self, ind):
        fit1 = numpy.array(self.fitness)
        fit2 = numpy.array(ind.fitness)
        
        return numpy.linalg.norm(fit1 - fit2)
    
    def to_dict(self):
        return {'fitness': self.fitness,
                'chromosome': self.fitness}
    
    def to_dict_fitness(self):
        return {'f1': self.fitness[0],
                'f2': self.fitness[1]}
    
    def show(self):
        pass

    @staticmethod
    def create_chromosome(length):
        chromosome = []
        for i in range(length):
            chromosome.append(1 if random.random() <= 0.5 else 0)
        return chromosome

class IndividualMRP(Individual):
    
    def __init__(self):
        super(IndividualMRP, self).__init__()
        self.paths = []

        self.delay = 0.0
        self.loss = 0.0
        self.bandwidth = INF
        
    def copy(self):
        # ind = self.__class__()
        ind = IndividualMRP()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)
        ind.paths = copy.deepcopy(self.paths)
        ind.delay = self.delay
        ind.loss = self.loss
        ind.bandwidth = self.bandwidth
        ind.crowding_distance = self.crowding_distance
        ind.pareto_rank = self.pareto_rank

        return ind

    def initialize(self, chromosome, problem):
        self.chromosome = chromosome
        self.problem = problem
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
            graph.add_edge(link.src, link.dst, delay=link.delay, band=link.bandwidth, loss=link.loss)
        
        if state:
            if mrp.src not in graph.node: state = False
            else:
                for dst in mrp.dst:
                    if dst not in graph.node: state = False
        
        # if state: state = True if nx.is_connected(graph) else False
        
        if state:
            for dst in mrp.dst:
                if not nx.has_path(graph,source=mrp.src,target=dst):
                    state = False
        
        if state: self._init_tree_by_subgraph(self.problem, graph)
        else:
            # self.delay = INF
            # self.loss = INF
            self.delay = float(500)
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
                delay += graph.edge[path[index]][path[index + 1]]['delay']
                loss *= 1 - graph.edge[path[index]][path[index + 1]]['loss']
                if self.bandwidth > graph.edge[path[index]][path[index + 1]]['band']:
                    self.bandwidth = graph.edge[path[index]][path[index + 1]]['band']
                    
            max_delay += delay
            max_loss += 1 - loss
        
        self.delay = float(max_delay / len(mrp.dst))
        self.loss = float(max_loss / len(mrp.dst))

    def is_dominated(self, ind):
        if ind.loss <= self.loss and ind.delay < self.delay:
            return True
        elif ind.loss < self.loss and ind.delay <= self.delay:
            return True
        return False

    def crossover(self, ind):
        temp = self.create_chromosome(self.problem.num_link)
        for i in range(len(temp)):
            if temp[i]:
                obj = self.chromosome[i]
                self.chromosome[i] = ind.chromosome[i]
                ind.chromosome[i] = obj
    
        # self.fitness = self.cal_fitness()
        # ind.fitness = ind.cal_fitness()

    def mutation(self):
        for i in range(len(self.chromosome)):
            self.chromosome[i] = 1 - self.chromosome[i] \
                if random.random() < PM else self.chromosome[i]
    
        self.fitness = self.cal_fitness()
    
    def to_dict(self):
        return {
            'delay': self.delay,
            'loss': self.loss,
            'bandwidth': self.bandwidth,
            'paths': str(self.paths)
        }


class IndividualKP(Individual):

    def __init__(self):
        super(IndividualKP, self).__init__()
        
        
    def copy(self):
        ind = IndividualKP()
        ind.problem = self.problem
        ind.chromosome = copy.copy(self.chromosome)
        ind.fitness = copy.copy(self.fitness)
        return ind
    
    def initialize(self, chromosome, problem):
        self.problem = problem
        self.chromosome = chromosome
        self.fitness = self.cal_fitness(chromosome)
    #
    
    def cal_fitness(self, chromosome):
        profits = []
        weights = []
        ratios = []
        
        for x in range(2):
            profit = []
            weight = []
            ratio = []
            for y in range(len(chromosome)):
                if chromosome[y]:
                    profit.append(self.problem[x]['items'][y]['profit'])
                    weight.append(self.problem[x]['items'][y]['weight'])
                    ratio.append(self.problem[x]['items'][y]['ratio'])
                    
            profits.append(profit)
            weights.append(weight)
            ratios.append(ratio)
            
        capacity = [self.problem[0]['capacity'], self.problem[1]['capacity']]
        self.greedy_repair_heuristic(profits, weights, ratios, capacity, chromosome)
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
                