import matplotlib.pyplot as plt
import os
import numpy as np

def dis_plot(q):
    if q == 2:
        upper = 0.4
    else:
        upper = 0.11
    with open(f"./results_{q}_0.5.txt", 'r') as f:
        data = f.readlines()[0].replace("[", "").replace("]", "").replace(",", " ").split()
        y1 = list(map(lambda x: float(x), data))
    with open(f"./results_{q}_1.0.txt", 'r') as f:
        data = f.readlines()[0].replace("[", "").replace("]", "").replace(",", " ").split()
        y2 = list(map(lambda x: float(x), data))
    x = np.linspace(0.0, upper, len(data))
    plt.title(f"Phase diagram. N = 10^5, q = {q}")
    plt.plot(x, y1, "o", markersize=4, label=f"c(0) = 0.5")
    plt.plot(x, y2, "v", markersize=4, label=f"c(0) = 1.0")
    plt.xlabel("p")
    plt.ylabel("c")
    plt.ylim(0,1)
    plt.legend()
    plt.show()

dis_plot(2)
dis_plot(8)
# dis_plot(200, 2, 1)
# dis_plot(200, 8, 0.5)
# dis_plot(200, 8, 1)
