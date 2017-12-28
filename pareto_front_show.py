from algorithm.util import *

topo = 'topo4'


if __name__ == '__main__':
    # plot_ps_by_different_algorithm(topo,
    #                                ['MOEAD-SFLA', 'MOEAD-OBL', 'MOEAD', 'NSGA-II', 'IDEAL'], topo)

    plot_ps_by_different_algorithm(topo, ['SPEA2', 'IDEAL'], 'SPEA2 -- Topo4')
