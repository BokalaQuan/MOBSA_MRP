from algorithm.individual import IndividualMRP
from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP

import copy

if __name__ == '__main__':
    topo = 'topo4'
    test = MRP()
    test.initialize(topo)

    good = 0
    bad = 0
    same = 0
    equal = 0
    tmp = 0

    for i in range(200):
        ind = IndividualMRP()
        ind.init_ind(test)
        # while not ind.is_feasible():
        #     ind.init_ind(test)
        ind1 = ind.copy()
        # fit1 = copy.copy(ind.fitness)
        ind.opposition_based_learning()
        # fit2 = copy.copy(ind.fitness)

        if ind1.is_feasible():
            tmp += 1


        if ind <= ind1:
            good += 1
            # print "Opposition Learning Success."
        elif ind >= ind1:
            bad += 1
            # print "Failure."
        elif ind == ind1:
            same += 1
            # print "Same."
        else:
            equal += 1

    print "Good = ", good, " , Bad = ", bad, " , Same = ", same, " , Equal = ", equal
    print "Feasible = ", tmp