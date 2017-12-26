import matplotlib.pyplot as plt
import numpy as np

import random

if __name__ == '__main__':

    x = [random.randint(0, 50) for i in range(50)]
    y = [random.randint(6, 66) for i in range(50)]


    plt.figure()
    plt.scatter(x, y, alpha=0.5)
    plt.show()
