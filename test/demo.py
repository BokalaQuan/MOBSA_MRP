from problem.mrp.multicast_routing_problem import MulticastRoutingProblem as MRP
from mobsa import IndividualBeetle

import numpy
import random
import os
import json
import networkx as nx
import matplotlib.pyplot as plot


if __name__ == '__main__':
    
    graph = nx.waxman_graph(50,alpha=0.4, beta=0.2)
    
    file_name = os.getcwd() + '\\node.json'
    with open(file_name, 'w') as f:
        f.write(json.dumps(graph.node, indent=4))
        f.close()

    file_name = os.getcwd() + '\\edge.json'
    with open(file_name, 'w') as f:
        f.write(json.dumps(graph.edge, indent=4))
        f.close()
    
    print nx.nx_pylab.draw(graph)