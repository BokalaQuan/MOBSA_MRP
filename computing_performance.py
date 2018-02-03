from algorithm.util import *

"""
Rand_Topo = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
SNDlib_Topo = ['cost266', 'france', 'geant', 'germany50', 'india35', 'newyork', 
               'pioro40', 'ta1', 'ta2']
Zoo_Topo = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica', 'Chinanet', 
            'Dfn', 'Geant2012', 'HiberniaGlobal', 'Highwinds', 'HurricaneElectric', 
            'Internetmci', 'Rediris', 'Tinet', 'Uninett2011', 'Uunet']
"""

if __name__ == '__main__':
    topo = 'ta2'
    al_lst = ['EAG-MOEAD', 'NSABC', 'MOEAD', 'MOEAD-OBL', 'MOEAD-SFLA', 'NSGA-II']

    GD_ = []
    IGD_ = []
    HV_ = []

    for al in al_lst[:1]:
        METRIC, GD, IGD, HV = cal_metric(topo=topo, runtime=20, algorithm=al)
        write_metric(topo=topo, algorithm=al, metric=METRIC)
        # GD_.append(GD)
        # IGD_.append(IGD)
        # HV_.append(HV)
    # plot_performance_as_boxplot(topo=topo, metric='GD', algorithms=al_lst, lst=GD_)
    # plot_performance_as_boxplot(topo=topo, metric='IGD', algorithms=al_lst, lst=IGD_)
    # plot_performance_as_boxplot(topo=topo, metric='HV', algorithms=al_lst, lst=HV_)
#
