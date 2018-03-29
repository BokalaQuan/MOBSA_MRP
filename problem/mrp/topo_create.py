from problem.mrp.multicast_routing_problem import *

import networkx as nx
import json
import os
import random
import matplotlib.pyplot as plt


def create_topology(path, filename, pattern=None):
    """

    :param path:
    :param pattern: pattern default is "RAND".
    :return:
    """
    if pattern == 'GML':
        G = nx.read_gml(path=path+'/'+filename+'.gml', label='id')
    else:
        G = nx.fast_gnp_random_graph(n=200, p=0.025)
        plt.figure()
        nx.draw(G, with_labels=True, node_size=40, node_color='k',
                font_size=4, font_color='w')
        # plt.show()
        plt.savefig(path+'/'+filename+".png", dpi=900)



    # plt.figure()
    # nx.draw(G, with_labels=True, node_size=100, node_color='k',
    #         font_size=8, font_color='w')
    # plt.show()

    node_list = []
    edge_list = []

    for item in G.nodes:
        sw = {"dpid": item,
              "attribute": str('custom'),
              "name": get_switch_dpid(int(item)+1)}
        node_list.append(sw)

    src = random.randint(1, len(node_list)-1)
    dst = []

    node_list[src]["attribute"] = str('source')

    while len(dst) < 8:
        ran = random.randint(0, len(node_list) - 1)
        if ran not in dst and ran is not src:
            dst.append(ran)
            node_list[ran]["attribute"] = str('destination')

    for item in G.edges():
        src = item[0]
        dst = item[1]
        delay = float('%.3f' % random.uniform(0.1,10.0))
        loss = float('%.3f' % random.uniform(0.001,0.1))
        bandwidth = int(random.uniform(1,20)) * 10

        link = {"src": src,
                "dst": dst,
                "delay": delay,
                "loss": loss,
                "bandwidth": bandwidth}

        edge_list.append(link)

    with open(path+'/switch_info.json', 'wb') as f:
        f.write(json.dumps(node_list, indent=4, sort_keys=True))
        f.close()

    with open(path+'/link_info.json', 'wb') as f:
        f.write(json.dumps(edge_list, indent=4, sort_keys=True))
        f.close()

    print ("Topo ", filename, " create succeed!")

def get_switch_dpid(number):
    prefix = "00"
    if number >= int(100):
        prefix = ""
    elif number >= int(10):
        prefix = "0"

    return 's' + prefix + str(number)

def get_host_dpid(number):
    prefix = "00"
    if number >= int(100):
        prefix = ""
    elif number >= int(10):
        prefix = "0"

    return 'h' + prefix + str(number)



if __name__ == '__main__':

    name = 'Rand8'
    # path = os.getcwd() + '/Zoo_Topo/' + name
    # create_topology(path=path, filename=name,pattern='GML')

    path = os.getcwd() + '/Rand_Topo/' + name
    create_topology(path=path, filename=name)
