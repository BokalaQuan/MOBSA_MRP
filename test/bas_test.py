import networkx as nx
import matplotlib.pyplot as plt
import random

# G = nx.fast_gnp_random_graph(100, 0.05)
# nx.draw_networkx(G,pos=nx.spring_layout(G))
# plt.show()

class A(object):
    def __init__(self):
        self.id = random.randint(0, 100)

temp = []
for i in range(5):
    a = A()
    temp.append(a)
    
temp_b = []
temp_b.extend(temp)

print "A"
print [id(x) for x in temp]

print "B"
print [id(x) for x in temp_b]


temp = []
print "B"
print [id(x) for x in temp_b]
    
