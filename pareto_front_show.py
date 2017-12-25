from algorithm.util import *

topo = 'topo6'

# plot_ps_by_same_algorithm(topo, 'NSGA-II', 5)

if __name__ == '__main__':
    # plot_ps_by_different_algorithm(topo, ['MOEAD', 'MOEAD-SFLA', 'MOEAD-OBL', 'NSGA-II'], topo)
    # plot_ps_by_different_algorithm(topo, ['MOEAD', 'MOEAD-SFLA',  'NSGA-II'], topo)
    plot_ps_by_different_algorithm(topo, ['MOEAD-SFLA', 'MOEAD-OBL', 'MOEAD'], topo)
    # plot_ps_by_different_algorithm(topo, ['MOEAD',  'MOEAD-OBL'], topo)

