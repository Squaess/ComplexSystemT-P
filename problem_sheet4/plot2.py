import matplotlib.pyplot as plt
import pickle
import os
import task2

if not os.path.exists("results2"):
    raise ValueError

def dis_plot(N, p, q, c):
    if p == 0.2:
        col = "r"
    else:
        col = ""
    with open(os.path.join("results2", f"{N}_{p}_{q}_{c}"), 'rb') as f:
        data1 = pickle.load(f)
    plt.title(f"Up spins concentration. q = 2, N = {N}, p = {p}, c = {c}")
    plt.plot(data1, col+"", label=f"p={p}", markersize=1)
    plt.xlabel("MCS")
    plt.ylabel("c")
    plt.ylim(0,1)
    plt.show()

INIT_C = task2.INIT_C1 + task2.INIT_C1
# for i in INIT_C:
#     dis_plot(200, 0.2, 2, i)

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

for i in INIT_C:
    dis_plot(500, 0.2, 2, i)

for i in INIT_C:
    dis_plot(500, 0.4, 2, i)