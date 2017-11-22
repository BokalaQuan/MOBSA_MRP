import json
import os
import random

PATH = os.path.split(os.path.realpath(__file__))[0]

class MulticastRoutingProblem(object):
    
    def __init__(self):
        self.switches = []
        self.links = []
        
        self.num_switch = 0
        self.num_link = 0
        
        self.src = None
        self.dst = []
    
    def initialize(self, filename):
        SWITCH_PATH = PATH + '\\topo_file\\' + filename + '\\switch_info.json'
        LINK_PATH = PATH + '\\topo_file\\' + filename + '\\link_info.json'
    
        with open(SWITCH_PATH, 'r') as f:
            conf = json.load(f)
            for item in conf:
                sw = Node(item)
                self.switches.append(sw)
                self.num_switch += 1
                if sw.attribute == str("source"): self.src = item["dpid"]
                elif sw.attribute == str("destination"): self.dst.append(item["dpid"])
        
            f.close()
    
        with open(LINK_PATH, 'r') as f:
            conf = json.load(f)
            for item in conf:
                link = Edge(item)
                self.links.append(link)
                self.num_link += 1
                
        f.close()
        
class Node(object):
    
    def __init__(self, switch):
        self.attribute = str(switch["attribute"])
        self.dpid = int(switch["dpid"])
        self.name = str(switch["name"])

class Edge(object):
    
    def __init__(self, link):
        self.src = int(link["src"])
        self.dst = int(link["dst"])
        self.delay = link["delay"]
        self.loss = link["loss"]
        # self.delay = random.random()
        # self.loss = random.random()
        self.bandwidth = link["bandwidth"]
                

if __name__ == '__main__':
    demo = MulticastRoutingProblem()
    demo.initialize('topo1')
    print demo.dst, demo.src
    