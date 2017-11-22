import os
import json
import random

PATH = os.path.split(os.path.realpath(__file__))[0]

class KnapsackProblem(object):
    
    def __init__(self):
        self.knapsack = []
    
        self.num_item = 0
        self.num_knap = 0
    
        
    def initialize(self, filename):
        FILE_PATH = PATH + '\\data\\' + filename
        with open(FILE_PATH, 'r') as f:
            conf = json.load(f)
            for item in conf:
                self.knapsack.append(item)
        
    