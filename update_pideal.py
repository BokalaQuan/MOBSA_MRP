from algorithm.util import *



if __name__ == '__main__':

    # topos = ['topo1', 'topo2', 'topo3', 'topo4', 'topo5', 'topo6']
    # al_lst = ['MOEAD', 'NSGA-II', 'MOEAD-OBL', 'MOEAD-SFLA', 'SPEA2']
    #
    # lst = read_json_as_list(topo=topos[4], algorithm=al_lst[4], runtime=20)
    # write_list_to_json(topo=topos[4], algorithm=al_lst[4], solutions=lst)
    #
    # for topo in topos:
    #     update_ideal_pf(topo=topo, algorithms=al_lst)

    topos = ['topo1', 'topo2', 'topo3', 'topo4', 'topo5', 'topo6']
    al = ['EAG-MOEAD', 'NSABC', 'MOEAD', 'MOEAD-OBL', 'MOEAD-SFLA', 'NSABC', 'NSGA-II']

    for topo in topos:
        update_ideal_pf(topo=topo, algorithms=al)
