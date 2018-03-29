from algorithm.util import *



if __name__ == '__main__':

    path = '/Rand_Topo/'
    # path = '/SNDlib_Topo/'
    # path = '/Zoo_Topo/'
    topos = ['Rand1', 'Rand2', 'Rand3', 'Rand4', 'Rand5', 'Rand6', 'Rand7', 'Rand8']
    # topos = ['cost266', 'france', 'geant', 'germany50', 'india35',
    #          'newyork', 'pioro40', 'ta1', 'ta2']
    # topos = ['AttMpls', 'Bellcanada', 'Bellsouth', 'BtNorthAmerica',
    #          'Chinanet', 'Dfn', 'Geant2012', 'HiberniaGlobal',
    #          'Highwinds', 'HurricaneElectric', 'Internetmci',
    #          'Rediris', 'Tinet', 'Uninett2011', 'Uunet']

    # topos = ['topo1', 'topo2', 'topo3', 'topo4', 'topo5', 'topo6']
    # al_lst = ['MOEAD', 'NSGA-II', 'MOEAD-OBL', 'MOEAD-SFLA', 'SPEA2']

    # alst = ['NSACO', 'PBIL', 'MOPSO', 'NSGA-II', 'MOEAD', 'EAG-MOEAD',
    #         'NSABC', 'SFLA-MOEAD', 'OBL-MOEAD']
    alst = ['Jaya', 'NSGA-II', 'MOEAD']

    runtime = 10

    for topo in topos[1:2]:
        for al in alst[:]:
            lst = []
            for i in range(runtime):
                lst.extend(read_json_as_list(topo=topo, algorithm=al, runtime=i+1))

            write_list_to_json(topo=topo, algorithm=al, solutions=lst)
        # update_ideal_pf(topo=topo, algorithms=alst)