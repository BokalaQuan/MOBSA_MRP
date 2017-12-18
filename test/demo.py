import numpy
import random
import os
import json
import networkx as nx
import matplotlib.pyplot as plot

if __name__ == '__main__':
    
    # graph = nx.waxman_graph(50,alpha=0.4, beta=0.2)
    graph = nx.fast_gnp_random_graph(20, 0.3)
    
    print graph.node
    
    print graph.edge
    
    graph.add_edge(1, 4, delay=10, cost=12)
    graph.add_edge(8, 4, delay=90)
    
    print graph.node[9].pos
    
    print graph.edge[1][4]
    print graph.edge[8][4]
    
    
    # path = os.getcwd()
    
    print nx.dijkstra_path(graph, source=10, target=6, weight='delay')
    
    nx.draw_networkx(graph)