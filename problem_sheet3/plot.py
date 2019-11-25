import matplotlib.pyplot as plt
import numpy as np
import pickle

import task

f_range = np.linspace(0.0, 0.99, 10)

def plot(name, attack=False):
    fig = plt.figure(figsize=(16,9))
    fig.suptitle(name, fontsize=16)
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
        plt.ylabel("prob giant component")
        plt.legend()
        pos += 1
    plt.show()
            
for name in task.NAMES:
    plot(name)
################################

            
            
