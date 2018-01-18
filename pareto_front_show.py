from algorithm.util import *

topo = 'topo1'


if __name__ == '__main__':
    # plot_ps_by_different_algorithm(topo,
    #                                ['MOEAD-SFLA', 'MOEAD-OBL', 'MOEAD', 'NSGA-II', 'IDEAL'], topo)

    plot_ps_by_different_algorithm(topo, ['EAG-MOEAD', 'NSABC', 'MOEAD',
                                          'MOEAD-OBL', 'MOEAD-SFLA', 'NSGA-II', "IDEAL"])

