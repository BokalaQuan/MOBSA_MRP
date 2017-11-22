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
        

if __name__ == '__main__':
    a = A()
    b = a.copy()
    
    print a is b