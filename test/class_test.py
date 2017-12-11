import random
import os

class A(object):
    
    def __init__(self):
        self.id = random.randint(0, 1000)
        self.name = A.__name__
    
    def copy(self):
        a = A()
        a.id = self.id
        a.name = self.name
        return a
    
    def show(self):
        print self.id, self.name

class B(A):
    
    def __init__(self):
        super(B, self).__init__()
        self.name = B.__name__
        
    def show(self, string):
        print self.id, self.name + string
        
def update(refer, pos):
    tmp = []
    for ref, p in zip(refer, pos):
        tmp.append(ref if ref < p else p)
    return tmp


if __name__ == '__main__':
    
    a = B()
    print type(a.__class__.__name__)