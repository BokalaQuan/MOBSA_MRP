from algorithm.parameter import EXTERNAL_ARCHIVE_SIZE, INF

import random
import copy


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
    for pareto_rank_set in pareto_rank_set_list:
        if pareto_rank_set is not None or len(pareto_rank_set) != 0:
            if len(pareto_rank_set) == 1:
                pareto_rank_set[0].crowding_distance = INF
            elif len(pareto_rank_set) == 2:
                pareto_rank_set[0].crowding_distance = INF
                pareto_rank_set[1].crowding_distance = INF
            else:
                for obj in range(2):
                    pareto_rank_set.sort(key=lambda x:x.fitness[obj])

                    pareto_rank_set[0].crowding_distance = INF
                    pareto_rank_set[-1].crowding_distance = INF

                    min_obj = pareto_rank_set[0].fitness[obj]
                    max_obj = pareto_rank_set[-1].fitness[obj]

                    if min_obj == max_obj:
                        max_obj += 1

                    for x in range(1, len(pareto_rank_set) - 1):
                        pareto_rank_set[x].crowding_distance += \
                            abs(float(pareto_rank_set[x - 1].fitness[obj] - pareto_rank_set[x + 1].fitness[obj]) / (max_obj - min_obj))

        pareto_rank_set.sort(key=lambda x:x.crowding_distance, reverse=True)


'''
@author Joshua Knowles, et al.
@title "Approximating the non-dominated front using the Pareto Archived Evolution Strategy."
@date 1999
'''
class HyperCube(object):
    
    def __init__(self, solution):
        self.num_grid = None
        self.solution = solution.copy()
        
    def update_cube(self, num_grid):
        self.num_grid = copy.copy(num_grid)

class AdaptiveGrid(object):
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.upper = [0.0, 0.0]
        self.lower = [INF, INF]
        self.grid = []
        self.p_select = []
        self.archive = []
    
    def init_grid(self, poplist):
        for ind in poplist:
            self.archive.append(HyperCube(ind))
        self.grid_adjust()
        
    def grid_adjust(self):
        self.clear_grid_property()
        for cube in self.archive:
            self.upper[0] = cube.solution.fitness[0] if cube.solution.fitness[0] > self.upper[0] \
                else self.upper[0]
            self.upper[1] = cube.solution.fitness[1] if cube.solution.fitness[1] > self.upper[1] \
                else self.upper[1]
            self.lower[0] = cube.solution.fitness[0] if cube.solution.fitness[0] < self.lower[0] \
                else self.lower[0]
            self.lower[1] = cube.solution.fitness[1] if cube.solution.fitness[1] < self.lower[1] \
                else self.lower[1]
    
        mod = [float(self.upper[0] - self.lower[0]) / self.grid_size,
               float(self.upper[1] - self.lower[1]) / self.grid_size]
    
        for cube in self.archive:
            cube.num_grid = [int((cube.solution.fitness[0] - self.lower[0]) / mod[0]),
                             int((cube.solution.fitness[1] - self.lower[1]) / mod[1])]
    
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cubes = []
                for index in range(len(self.archive)):
                    if self.archive[index].num_grid == [i, j]:
                        cubes.append(self.archive[index])
            
                if len(cubes) != 0:
                    self.grid.append(cubes)
                    self.p_select.append(len(cubes))
        
        if len(self.archive) > EXTERNAL_ARCHIVE_SIZE:
            index_select = max(self.p_select)
            tmp = random.randint(0, len(self.grid[index_select])-1)
            self.grid[index_select].pop(tmp)
        
                    
    def update_grid(self, ind):
        flag = 0
        for i in range(len(self.archive)):
            if ind >=self.archive[i].solution or \
                    ind == self.archive[i].solution:
                flag += 1
            elif self.archive[i].solution >= ind:
                self.archive.pop(i)
                i -= 1
                
        if flag != 0:
            self.archive.append(HyperCube(ind))
        
        self.grid_adjust()
        
    def clear_grid_property(self):
        self.grid = []
        self.upper = [0.0, 0.0]
        self.lower = [INF, INF]
        self.p_select = []
