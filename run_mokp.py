from problem.kp.knapsack_problem import MultiObjectiveKnapsackProblem as MOKP

from moead import MultiObjectiveEvolutionaryAlgorithmBasedOnDecomposition as MOEAD

import os
import time


if __name__ == '__main__':

    ins = '50_2.json'
    problem = MOKP()
    problem.initialize(ins)

    print problem.num_item, problem.num_knap
