"""
Population-Based Evolutionary Algorithm
"""

from algorithm.individual import Individual

class Human(Individual):

    def __init__(self):
        super(Human, self).__init__()
        # The sex is choose in Male or Female
        self.sex = None
        # The man's social property
        self.ps = None
        # The man's natural property
        self.pn = None

    def __str__(self):
        return "id = " + str(id(self)) + ", Fitness = " + str(self.fitness) \
               + ", Sex = " + self.sex


class PopulationBasedEvolutionaryAlgorithm(object):

    def __init__(self):
        pass


if __name__ == '__main__':

    import numpy as np
    import matplotlib.pyplot as plt

    f = lambda x:1 / np.exp(x)

    plt.figure()
    x = range(1, 100, 1)
    y = [f(c) for c in x]

    plt.plot(x,y)
    plt.show()
