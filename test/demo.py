import numpy as np
import random
import os
import json
import networkx as nx
import matplotlib.pyplot as plot
import math


if __name__ == '__main__':

    from algorithm.util import func_levy as levy

    x = levy(5, 1)

    print(x)
    print(x*[2,2,2,2,2])