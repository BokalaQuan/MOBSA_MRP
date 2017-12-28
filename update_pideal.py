from algorithm.util import *



if __name__ == '__main__':

    topos = ['topo1', 'topo2', 'topo3', 'topo4', 'topo5', 'topo6']
    al_lst = ['MOEAD', 'NSGA-II', 'MOEAD-OBL', 'MOEAD-SFLA', 'SPEA2']

    lst = read_json_as_list(topo=topos[3], algorithm=al_lst[4], runtime=1)
    write_list_to_json(topo=topos[3], algorithm=al_lst[4], solutions=lst)
    #
    # for topo in topos:
    #     update_ideal_pf(topo=topo, algorithms=al_lst)