from algorithm.util import *

"""
Rand_Topo = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
SNDlib_Topo = ['cost266', 'france', 'geant', 'germany50', 'india35', 'newyork', 
               'pioro40', 'ta1', 'ta2', 'zib54']
Zoo_Topo = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica', 'Chinanet', 
            'Dfn', 'Geant2012', 'HiberniaGlobal', 'Highwinds', 'HurricaneElectric', 
            'Internetmci', 'Rediris', 'Tinet', 'Uninett2011', 'Uunet']
"""

# topo = 'Rand4'


if __name__ == '__main__':
    # topo_lst = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topo_lst = ['germany50', 'india35', 'ta1', 'ta2']
    topo_lst = ['AttMpls', 'BtNorthAmerica', 'HiberniaGlobal', 'Tinet']

    alst = ['NSABC', 'MOEA-PCGG', 'SPEA2', 'MOEAD', 'EAG-MOEAD', 'MOSFLA']

    # tlst = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']
    # tlst = ['S1', 'S2', 'S3', 'S4']
    tlst = ['Z1', 'Z2', 'Z3', 'Z4']

    for topo, title in zip(topo_lst, tlst):

        plot_ps_by_different_algorithm(topo, alst, title=title)
    #
    # plot_ps_by_different_algorithm(topo='Rand1', algorithms=alst)
