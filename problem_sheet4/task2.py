import networkx as nx
import numpy as np
import numba
from numba import jit

N = 2* 10**5
p = 0.2
q = 2
avg_d = 14

g = nx.fast_gnp_random_graph(N, avg_d/(N-1))
states = np.full([N], 1)


@jit(nopython=True)
def agent_move(node, p, q, states, neighbours):
    if np.random.random_sample() < p:
        if np.random.random_sample() < 0.5:
            states[node] = states[node]*(-1)
    else:
        voters = np.random.choice(neighbours, q, replace=False)
        S = 0
        for i in voters:
            S += states[i]
        if S == q:
            states[i] = 1
        elif S == -q:
            states[i] = -1

for i in range(N):
    node = np.random.randint(0, N)
    neigh = np.array(list(g.adj[node]))
    agent_move(node, p, q, states, neigh)

print(states)

