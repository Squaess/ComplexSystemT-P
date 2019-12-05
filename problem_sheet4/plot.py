import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import task1

if not os.path.exists("results"):
    raise OSError("Could find result directory")

name_display = dict(
        random="Random graph",
        ws="Watts-Strogatz graph",
        ba="Barabsi-Alber graph"
    )

method_trans = dict(
    cc="closeness centrality",
    bc="betweenness centrality"
)

def plot(name, method):
    fig = plt.figure(figsize=(16,10))
    fig.suptitle(name_display.get(name) + " " + method_trans.get(method), fontsize=16)
    pos = 131
    for k in task1.AVG_K:
        plt.subplot(pos)
        plt.title(f"Average degree: {k}")
        for size in task1.SIZES:
            with open(os.path.join("results", f"{name}_{method}_{size}_{k}"), "rb") as f:
                f_range, results = zip(*pickle.load(f))
            plt.plot(f_range, results, 'o', label=f"N = {size}")
        plt.xlabel("f")
        plt.ylabel("prob giant component normalized")
        plt.legend()
        pos += 1
    plt.show()
            
            

for name in ["ws", "ba", "random"]:
    plot(name, "cc")
for name in ["ws", "ba", "random"]:
    plot(name, "bc")
################################

            
            
