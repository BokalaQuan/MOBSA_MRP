from algorithm.util import *

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    x = np.arange(-10, 10, 0.1)
    tmp = [func_tanh(i) for i in x]
    y = np.array(tmp)
    tmp = [func_trans_V1(i) for i in x]
    y1 = np.array(tmp)

    plt.plot(x, y)
    plt.plot(x, y1)
    plt.show()