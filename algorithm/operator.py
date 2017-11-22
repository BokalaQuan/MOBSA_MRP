import random
import copy
import math

INF = float('inf')

def fast_nondominated_sort(poplist):
    pareto_rank_set_list = []
    first_pareto_rank_set = []

    for ind in poplist:
        ind.clear_property()

    for ind_pre in poplist:
        for ind_beh in poplist:
            if ind_beh.is_dominated(ind_pre):
                ind_pre.dominating_list.append(ind_beh)
            elif ind_pre.is_dominated(ind_beh):
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
                    object_shell_sort(pareto_rank_set, obj)

                    pareto_rank_set[0].crowding_distance = INF
                    pareto_rank_set[len(pareto_rank_set) - 1].crowding_distance = INF

                    min_obj = pareto_rank_set[0].fitness[obj]
                    max_obj = pareto_rank_set[len(pareto_rank_set) - 1].fitness[obj]

                    if min_obj == max_obj:
                        max_obj += 1

                    for x in range(1, len(pareto_rank_set) - 1):
                        pareto_rank_set[x].crowding_distance += \
                            abs(float(pareto_rank_set[x - 1].fitness[obj] - pareto_rank_set[x + 1].fitness[obj]) / (max_obj - min_obj))

        object_shell_sort(pareto_rank_set, 'cd')


def object_merge_sort(lst, obj):
    if (len(lst) <= 1): return lst
    left = object_merge_sort(lst[:len(lst) / 2], obj)
    right = object_merge_sort(lst[len(lst) / 2:len(lst)], obj)
    result = []
    while len(left) > 0 and len(right) > 0:
        # if (left[0] > right[0]):
        if compare_to(left[0], right[0], obj):
            result.append(copy.deepcopy(right.pop(0)))
        else:
            result.append(copy.deepcopy(left.pop(0)))

    if (len(left) > 0):
        result.extend(copy.deepcopy(object_merge_sort(left, obj)))
    else:
        result.extend(copy.deepcopy(object_merge_sort(right, obj)))
    return result

def compare_to(ind0, ind1, obj):
    if obj == 0:
        if ind0.fitness[0] > ind1.fitness[0]:
            return True
    elif obj == 1:
        if ind0.fitness[1] > ind1.fitness[1]:
            return True
    elif obj == 'cd':
        if ind0.crowding_distance < ind1.crowding_distance:
            return True
    elif obj == 'mofitness':
        if ind0.mofitness < ind1.mofitness:
            return True
    elif obj == 'loss':
        if ind0['loss'] > ind1['loss']:
            return True

    return False


def object_shell_sort(lst, obj):
    count = len(lst) / 2
    while count > 0:
        for i in range(count, len(lst)):
            val = lst[i]
            j = i
            while j >= count and compare_to(lst[j - count], val, obj):
                lst[j] = lst[j - count]
                j -= count
            lst[j] = val
        count /= 2
