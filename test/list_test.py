import random
import os
from datetime import datetime

class Demo(object):
    
    def __init__(self, name):
        self.name = name
        self.id = random.uniform(1000, 10000)
        

if __name__ == '__main__':
    
    ll = []
    for i in range(5):
        ll.append(Demo(str(datetime.now())))
    
    x = []
    x.extend(ll)
    
    x[0].id = 110
    print id(x[0]), id(ll[0])
    