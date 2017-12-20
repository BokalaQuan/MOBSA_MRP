from algorithm.util import *

topo = 'topo1'

# plot_ps_by_same_algorithm(topo, 'NSGA-II', 5)

if __name__ == '__main__':
    plot_ps_by_different_algorithm(topo, ['MOEAD', 'NSGA-II'], topo)

