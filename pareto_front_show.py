from algorithm.util import *

"""
Rand_Topo = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
SNDlib_Topo = ['cost266', 'france', 'geant', 'germany50', 'india35', 'newyork', 
               'pioro40', 'ta1', 'ta2', 'zib54']
Zoo_Topo = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica', 'Chinanet', 
            'Dfn', 'Geant2012', 'HiberniaGlobal', 'Highwinds', 'HurricaneElectric', 
            'Internetmci', 'Rediris', 'Tinet', 'Uninett2011', 'Uunet']
"""

topo = 'Rand2'


if __name__ == '__main__':
    # alst = ['NSACO', 'PBIL', 'MOPSO', 'NSGA-II', 'MOEAD', 'EAG-MOEAD', 'NSABC', 'SFLA-MOEAD', 'OBL-MOEAD']

    alst = ['Jaya', 'NSGA-II', 'MOEAD']
    plot_ps_by_different_algorithm(topo, alst)

