import sys
import matplotlib.pyplot as plt
import os
import logging
import pickle
import numpy as np
import numba
# from numba import jit, njit
# from numba.typed import List
from igraph import Graph

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

MCS_STEPS = 1000

# @jit(nopython=False)
def agent_move(node, p, q, states, neighbours):
    if np.random.random_sample() < p:
        if np.random.random_sample() < 0.5:
            states[node] = states[node]*(-1)
    else:
        if len(neighbours) < q:
            return
        voters = np.random.choice(neighbours, q, replace=False)
        S = 0
        for i in voters:
            S += states[i]
        if S == q:
            states[node] = 1
        elif S == -q:
            states[node] = -1

# @jit(nopython=False)
def mcs(adj_l, N, p, q, states):
    for _ in range(N):
        # choose random node
        node = np.random.randint(0, N)
        neigh = adj_l[node]
        agent_move(node, p, q, states, neigh)
    # return calc_conc(states, N)

# @jit(nopython=False)
def simulate(adj_l, states, N, p, q, mcs_steps):
    for _ in range(mcs_steps):
        mcs(adj_l, N, p, q, states)
    return calc_conc(states, N)

# @jit(nopython=False)
def gen_states(N, c):
    rang = np.array([x for x in range(N)])
    states = np.array([-1 for x in rang])
    for x in np.random.choice(rang, int(c * N), replace=False):
        states[x] = 1
    return states

# @jit(nopython=False)
def calc_conc(states, N):
    return (1/(2*N)) * states.sum() + (1/2)

def save_results(N, q, c, result, p=100):
    logger.info("Saving results...")
    result = [x for x in result]
    if not os.path.exists("results3"):
        os.mkdir("results3")
    if p == 100:
        with open(f"results3/{N}_{q}_{c}", "wb+") as f:
            pickle.dump(result, f)
    else:
        with open(f"results3/{N}_{q}_{c}_{p}", "wb+") as f:
            pickle.dump(result, f)

def pyth_wrapper(N, p, q, avg_d, c):
    # Create graph and needed adj_list
    g = Graph.Erdos_Renyi(N, avg_d/(N-1))
    logger.info(f"Generating adj list for N={N}, p={p}, init_c = {c}, q={q}...")
    adj_l = []
    for x in g.get_adjlist():
        adj_l.append(np.array(x))
    logger.info("Creting adj list is done!!")
    states = gen_states(N, c)
    logger.info("Starting simulation...")
    return simulate(adj_l, states, N, p, q, MCS_STEPS)
    

if __name__ == "__main__":
    logger.info("Strarting simulation.")
    if len(sys.argv) != 4:
        ## INPUT: N, q, c
        raise ValueError
    else:
        concentration = list()
        for p in np.linspace(0.0, 1.0, 20):
            res = pyth_wrapper(
                N=int(sys.argv[1]),
                p=p,
                q=int(sys.argv[2]),
                avg_d=14,
                c=float(sys.argv[3])
            )
            logger.info(f"Result = {res}")
            save_results(
                sys.argv[1],
                sys.argv[2],
                sys.argv[3],
                concentration,
                p=p
            )
            concentration.append(res)
        save_results(sys.argv[1], sys.argv[2], sys.argv[3], concentration)