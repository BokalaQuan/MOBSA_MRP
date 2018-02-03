from algorithm.parameter import EXTERNAL_ARCHIVE_SIZE, INF

import random
import copy
import numpy as np


'''
@author K. Deb, et al.
@title "A fast and elitist multiobjective genetic algorithm: NSGA-II".
@date 2002.
'''
def fast_nondominated_sort(poplist):
    pareto_rank_set_list = []
    first_pareto_rank_set = []

    for ind in poplist:
        ind.clear_dominated_property()

    for ind_pre in poplist:
        for ind_beh in poplist:
            if ind_beh >= ind_pre:
                ind_pre.dominating_list.append(ind_beh)
            elif ind_beh <= ind_pre:
                ind_pre.num_dominated += 1

        if not ind_pre.num_dominated:
            ind_pre.pareto_rank = 0
            first_pareto_rank_set.append(ind_pre)

    pareto_rank_set_list.append(first_pareto_rank_set)
    rank = 0

    while pareto_rank_set_list[rank]:
        pareto_rank_set = []

        for ind in pareto_rank_set_list[rank]:
            for ind_dom in ind.dominating_list:
                ind_dom.num_dominated -= 1

                if not ind_dom.num_dominated:
                    ind_dom.pareto_rank = rank + 1
                    pareto_rank_set.append(ind_dom)

        if pareto_rank_set:
            rank += 1
            pareto_rank_set_list.append(pareto_rank_set)
        else:
            break

    return pareto_rank_set_list

'''
@author K. Deb, et al.
@title "A fast and elitist multiobjective genetic algorithm: NSGA-II".
@date 2002.
'''
def crowding_distance_sort(pareto_rank_set_list):
    if type(pareto_rank_set_list[0]) is list:
        for pareto_rank_set in pareto_rank_set_list:
            if pareto_rank_set is not None or len(pareto_rank_set) != 0:
                if len(pareto_rank_set) == 1:
                    pareto_rank_set[0].crowding_distance = INF
                elif len(pareto_rank_set) == 2:
                    pareto_rank_set[0].crowding_distance = INF
                    pareto_rank_set[1].crowding_distance = INF
                else:
                    for obj in range(2):
                        pareto_rank_set.sort(key=lambda x: x.fitness[obj])

                        pareto_rank_set[0].crowding_distance = INF
                        pareto_rank_set[-1].crowding_distance = INF

                        min_obj = pareto_rank_set[0].fitness[obj]
                        max_obj = pareto_rank_set[-1].fitness[obj]

                        if min_obj == max_obj:
                            max_obj += 1

                        for x in range(1, len(pareto_rank_set) - 1):
                            pareto_rank_set[x].crowding_distance += \
                                abs(float(pareto_rank_set[x - 1].fitness[obj] -
                                          pareto_rank_set[x + 1].fitness[obj]) /
                                    (max_obj - min_obj))

            pareto_rank_set.sort(key=lambda x: x.crowding_distance, reverse=True)
    else:
        for obj in range(2):
            pareto_rank_set_list.sort(key=lambda x: x.fitness[obj])

            pareto_rank_set_list[0].crowding_distance = INF
            pareto_rank_set_list[-1].crowding_distance = INF

            min_obj = pareto_rank_set_list[0].fitness[obj]
            max_obj = pareto_rank_set_list[-1].fitness[obj]

            if min_obj == max_obj:
                max_obj += 1

            for x in range(1, len(pareto_rank_set_list) - 1):
                pareto_rank_set_list[x].crowding_distance += \
                    abs(float(pareto_rank_set_list[x - 1].fitness[obj] -
                              pareto_rank_set_list[x + 1].fitness[obj]) /
                        (max_obj - min_obj))

        pareto_rank_set_list.sort(key=lambda x: x.crowding_distance, reverse=True)


def make_new_population(poplist, popsize):
    new_pop = []
    pareto_rank_set_list = fast_nondominated_sort(poplist)
    crowding_distance_sort(pareto_rank_set_list)

    for pareto_rank_set in pareto_rank_set_list:
        if len(new_pop) < popsize:
            if (len(pareto_rank_set) + len(new_pop)) <= popsize:
                for ind in pareto_rank_set:
                    new_pop.append(ind.copy())
            else:
                current = len(new_pop)
                for i in range(popsize - current):
                    new_pop.append(pareto_rank_set[i].copy())

    return new_pop


def select_solution_in_bidding_competition(poplist):
    length = len(poplist)

    index1, index2 = 0, 0
    while index1 == index2:
        index1, index2 = random.randint(0, length-1), random.randint(0, length-1)

    ind1 = poplist[index1]
    ind2 = poplist[index2]

    if ind1 <= ind2:
        return ind1
    elif ind2 <= ind1:
        return ind2
    else:
        return ind1 if random.random() < 0.5 else ind2


'''
@author Joshua Knowles, et al.
@title "Approximating the non-dominated front using the Pareto Archived Evolution Strategy."
@date 1999
'''
class HyperCube(object):
    
    def __init__(self, solution):
        self.coordinate = None
        self.solution = solution.copy()
        
class AdaptiveGrid(object):
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = []
        self.p_select = []
        self.archive = []
    
    def init_grid(self, poplist):
        for ind in poplist:
            self.archive.append(HyperCube(ind))

        if len(poplist) > EXTERNAL_ARCHIVE_SIZE:
            self.grid_adjust()

    def get_solution(self):
        if len(self.archive) < EXTERNAL_ARCHIVE_SIZE:
            index = random.randint(0, len(self.archive)-1)
            return self.archive[index].solution
        else:
            p_lst = []
            for p in self.p_select:
                tmp = p/sum(self.p_select)
                p_lst.append(tmp+sum(p_lst))

            ran = random.random()
            if ran <= p_lst[0]:
                return self.grid[0][random.randint(0,len(self.grid[0])-1)].solution
            else:
                for j in range(1, len(p_lst)):
                    if ran > p_lst[j-1] and ran <= p_lst[j]:
                        return self.grid[j][random.randint(0,len(self.grid[0])-1)].solution

    def get_solutions(self):
        return [cube.solution for cube in self.archive]

    def grid_adjust(self):
        self.grid = []
        self.p_select = []
        f_list = []
        for cube in self.archive:
            f_list.append(cube.solution.fitness)

        tmp = np.array(f_list)
        f_max = [max(tmp[:,0]), max(tmp[:,1])]
        f_min = [min(tmp[:,0]), min(tmp[:,1])]

        upper = [f_max[0] + (f_max[0] - f_min[0]) * 0.5 / self.grid_size,
                 f_max[1] + (f_max[1] - f_min[1]) * 0.5 / self.grid_size]
        lower = [f_min[0] - (f_max[0] - f_min[0]) * 0.5 / self.grid_size,
                 f_min[1] - (f_max[1] - f_min[1]) * 0.5 / self.grid_size]

        mod = [float(upper[0] - lower[0]) / self.grid_size,
               float(upper[1] - lower[1]) / self.grid_size]

        for cube in self.archive:
            cube.coordinate = [int((cube.solution.fitness[0] - lower[0]) / mod[0]),
                               int((cube.solution.fitness[1] - lower[1]) / mod[1])]
    
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cubes = []
                for index in range(len(self.archive)):
                    if self.archive[index].coordinate == [i, j]:
                        cubes.append(self.archive[index])
            
                if len(cubes) != 0:
                    self.grid.append(cubes)
                    self.p_select.append(len(cubes))
        
        while len(self.archive) > EXTERNAL_ARCHIVE_SIZE:
            index_select = self.p_select.index(max(self.p_select))
            tmp = random.randint(0, len(self.grid[index_select]) - 1)
            ind_del = self.grid[index_select][tmp]
            del(ind_del)
            self.p_select[index_select] -= 1
                    
    def update_grid(self, ind):
        if len(self.archive) == 0:
            self.archive.append(HyperCube(ind))

        else:
            flag = 0
            for arc in self.archive:

                if ind >= arc.solution or ind == arc.solution:
                    flag += 1
                elif arc.solution >= ind:
                    del(arc)

            if flag == 0:
                self.archive.append(HyperCube(ind))

            if len(self.archive) > EXTERNAL_ARCHIVE_SIZE:
                self.grid_adjust()
