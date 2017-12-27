from algorithm.util import *

topo = 'topo6'


if __name__ == '__main__':
    plot_ps_by_different_algorithm(topo,
                                   ['MOEAD-SFLA', 'MOEAD-OBL', 'MOEAD', 'NSGA-II', 'IDEAL'], topo)

