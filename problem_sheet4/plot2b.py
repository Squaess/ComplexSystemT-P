import matplotlib.pyplot as plt
import pickle
import os
import numpy as np
import task2b

if not os.path.exists("results3"):
    raise ValueError

def dis_plot(N, q, c):
    with open(os.path.join("results3", f"{N}_{q}_{c}"), 'rb') as f:
        data1 = pickle.load(f)
    plt.title(f"Up spins concentration. q = {q}, N = {N}, c = {c}")
    plt.plot(np.linspace(0.0, 0.1, len(data1)), data1, "o", markersize=1)
    plt.xlabel("p")
    plt.ylabel("c")
    plt.ylim(0,1)
    plt.show()

dis_plot(200, 2, 0.5)
dis_plot(200, 2, 1)
dis_plot(200, 8, 0.5)
dis_plot(200, 8, 1)
# for i in INIT_C:
#     dis_plot(200, 0.4, 2, i)

# for i in INIT_C:
#     dis_plot(100000, 0.2, 2, i)

# for i in INIT_C:
#     dis_plot(100000, 0.4, 2, i)

# for i in INIT_C:
#     dis_plot(1000, 0.2, 2, i)

# for i in INIT_C:
#     dis_plot(1000, 0.4, 2, i)

# for i in INIT_C:
#     dis_plot(500, 0.2, 2, i)

# for i in INIT_C:
#     dis_plot(500, 0.4, 2, i)