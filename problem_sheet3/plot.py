import tkinter
import matplotlib.pyplot as plt
import numpy as np
import pickle

import task

f_range = np.linspace(0.0, 0.99, 10)

name_display = dict(
        random="Random graphs",
        ws="Watts-Strogatz graph",
        ba="Barabsi-Alber graph"
    )

def plot(name, attack=False, save=False):
    fig = plt.figure(figsize=(16,10))
    #  fig = plt.figure()
    fig.suptitle(name_display.get(name) + " attack" if attack else name_display.get(name), fontsize=16)
    pos = 131
    for k in task.AVG_K:
        plt.subplot(pos)
        plt.title(f"Average degree: {k}")
        for size in task.SIZE:
            if attack:
                b = "attack"
            else:
                b = "results"
            with open(f"{b}_{name}_{size}_{k}", "rb") as f:
                results = pickle.load(f)
            plt.plot(f_range, results, 'o', label=f"N = {size}")
        plt.xlabel("f")
        plt.ylabel("prob giant component normalized")
        plt.legend()
        pos += 1
    if save:
        plt.savefig(f"{'attack' if attack else 'result'}_{name}")
    else:
        plt.show()
            
for name in task.NAMES:
    plot(name, attack=True)#, save=True)
for name in task.NAMES:
    plot(name, attack=False)#, save=True)
################################

            
            
