import json
import os

PATH = os.path.split(os.path.realpath(__file__))[0]

class MulticastRoutingProblem(object):
    
    def __init__(self):
        self.switches = []
        self.links = []
        
        self.num_switch = 0
        self.num_link = 0
        
        self.src = None
        self.dst = []
    
    def initialize(self, path, filename):
        SWITCH_PATH = PATH + path + filename + '/switch_info.json'
        LINK_PATH = PATH + path + filename + '/link_info.json'
    
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

        print "Topo " + filename + " initialized success!"
        print "Number of switches is ", self.num_switch, ", Number of links is ", self.num_link
        print "Source node is", self.src, ", Destination is ", self.dst
        
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
        self.bandwidth = link["bandwidth"]
