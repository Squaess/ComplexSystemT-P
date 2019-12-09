import matplotlib.pyplot as plt
import os
import numpy as np

def dis_plot(q, c):
    if q == 2:
        upper = 0.4
    else:
        upper = 0.11
    with open(f"./results_{q}_{c}.txt", 'r') as f:
        data = f.readlines()[0].replace("[", "").replace("]", "").replace(",", " ").split()
        y = list(map(lambda x: float(x), data))
    x = np.linspace(0.0, upper, len(data))
    plt.title(f"Up spins concentration. q = {q}, N =, c = {c}")
    plt.plot(x, y, "o", markersize=1)
    plt.xlabel("p")
    plt.ylabel("c")
    plt.ylim(0,1)
    plt.show()

# dis_plot(2, 0.5)
dis_plot(2, 1.0)
# dis_plot(8, 0.5)
dis_plot(8, 1.0)
# dis_plot(200, 2, 1)
# dis_plot(200, 8, 0.5)
# dis_plot(200, 8, 1)
