from algorithm.util import *



if __name__ == '__main__':

    topos = ['topo1', 'topo2', 'topo3', 'topo4', 'topo5', 'topo6']
    al_lst = ['MOEAD', 'NSGA-II', 'MOEAD-OBL', 'MOEAD-SFLA']

    # lst = read_json_as_list(topo=topos[5], algorithm=al_lst[3], runtime=20)
    # write_list_to_json(topo=topos[5], algorithm=al_lst[3], solutions=lst)

    for topo in topos:
        update_ideal_pf(topo=topo, algorithms=al_lst)