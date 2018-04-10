import sys
import networkx as nx
import json
import os
import random
import matplotlib.pyplot as plt

"""
Rand Topology parameter:

-----------------------------------------------------------------
| num_node | probability | node_size | font_size | destinations |
-----------------------------------------------------------------
|    50    |     0.09    |     50    |     5     |      7       |
-----------------------------------------------------------------
|    100   |     0.045   |     50    |     5     |      10      |
-----------------------------------------------------------------
|    200   |     0.03    |     45    |     4     |      14      |
-----------------------------------------------------------------
|    500   |     0.015   |     30    |     2.5   |      22      |
-----------------------------------------------------------------
"""

RANDs = {'Rand1': [50, 0.09, 50, 5, 7],
         'Rand2': [50, 0.09, 50, 5, 7],
         'Rand3': [100, 0.045, 50, 5, 10],
         'Rand4': [100, 0.045, 50, 5, 10],
         'Rand5': [200, 0.03, 45, 4, 14],
         'Rand6': [200, 0.03, 45, 4, 14],
         'Rand7': [500, 0.015, 30, 2.5, 22],
         'Rand8': [500, 0.015, 30, 2.5, 22]}


def create_topology(path, filename, pattern=None):
    """

    :param path:
    :param pattern: pattern default is "RAND".
    :return:
    """
    G = None

    if pattern == 'GML':
        G = nx.read_gml(path=path+'/'+filename+'.gml', label='id')
    else:
        # G = nx.fast_gnp_random_graph(n=50, p=0.09)
        G = nx.fast_gnp_random_graph(n=RANDs[filename][0], p=RANDs[filename][1])

    # node_color = ['k' for i in range(RANDs[filename][0])]

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

    while len(dst) < 7:
    # while len(dst) < RANDs[filename][-1]:
        ran = random.randint(0, len(node_list) - 1)
        if ran not in dst and ran is not src:
            dst.append(ran)
            node_list[ran]["attribute"] = str('destination')

    # node_color[src] = 'r'
    # for i in dst:
    #     node_color[i] = 'g'

    plt.figure()
    # nx.draw(G, with_labels=True, node_size=RANDs[filename][2], node_color=node_color,
    #         linewidths=0.5, font_size=RANDs[filename][3], font_color='w')

    nx.draw(G, with_labels=True, linewidths=0.5)
    # plt.show()
    plt.savefig(path + '/' + filename + ".png", dpi=600)


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

    with open(path + '/switch_info.json', 'w+') as f:
        f.write(json.dumps(node_list, indent=4, sort_keys=True))
        f.close()

    with open(path + '/link_info.json', 'w+') as f:
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

    name = 'HiberniaGlobal'
    path = os.getcwd() + '/Zoo_Topo/' + name

    create_topology(path=path, filename=name, pattern='GML')


    # if len(sys.argv) < 2:
    #     print("No input!!!")
    #     exit()
    #
    # name = sys.argv[1]

    # name = 'Rand1'
    # path = os.getcwd() + '/Zoo_Topo/' + name
    # create_topology(path=path, filename=name,pattern='GML')

    # path = os.getcwd() + '/Rand_Topo/' + name
    # create_topology(path=path, filename=name)
