"""
This code was used to produce task2 a plots.
"""

import sys
import matplotlib.pyplot as plt
import os
import logging
import pickle
import numpy as np
import numba
from numba import jit, njit
from numba.typed import List
from igraph import Graph

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

MCS_STEPS = 10000
INIT_C1 = [0.9, 0.8]#, 0.7, 0.6]
# INIT_C1 = [0.8]#, 0.7, 0.6]
INIT_C2 = [0.7, 0.6]
# INIT_C2 = [0.6]

@njit
def agent_move(node, p, q, states, neighbours):
    """ Make a move for a one agent
    Args:
        node (int): id of the node that we're concerning
        p (float) probability of independence
        q (int): how many neighbours we are choosing
        states: array of states for all nodes
        neighbours: array of neighbours for the node
    """
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

@njit
def mcs(adj_l, N, p, q, states):
    """ Perform one Monte carlo step
    """
    for _ in range(N):
        # choose random node
        node = np.random.randint(0, N)
        neigh = adj_l[node]
        agent_move(node, p, q, states, neigh)
    # return calc_conc(states, N)

@njit
def simulate(adj_l, states, N, p, q, mcs_steps):
    """ Perform mcs_steps MONTE CARLO STEP
    """
    result = List()
    for _ in range(mcs_steps):
        mcs(adj_l, N, p, q, states)
        result.append(calc_conc(states, N))
    return result

@njit
def gen_states(N, c):
    """  Generates inistial states for the graph with
    concentration of up spins 'c'
    """
    rang = np.array([x for x in range(N)])
    states = np.array([-1 for x in rang])
    for x in np.random.choice(rang, int(c * N), replace=False):
        states[x] = 1
    return states

@njit
def calc_conc(states, N):
    """ Calculate concentration of up spins from the
    states array
    """
    return (1/(2*N)) * states.sum() + (1/2)

def save_results(N, p, q, c, result):
    result = [x for x in result]
    if not os.path.exists("results2"):
        os.mkdir("results2")
    with open(f"results2/{N}_{p}_{q}_{c}", "wb+") as f:
        pickle.dump(result, f)

def pyth_wrapper(N, p, q, avg_d, c):
    # Create graph and needed adj_list
    g = Graph.Erdos_Renyi(N, avg_d/(N-1))
    logger.info(f"Generating adj list for N={N} ...")
    adj_l = List()
    for x in g.get_adjlist():
        adj_l.append(np.array(x))
    logger.info("Creting adj list is done!!")
    states = gen_states(N, c)
    logger.info("Starting simulation...")
    result = simulate(adj_l, states, N, p, q, MCS_STEPS)
    logger.info("Saving results...")
    save_results(N, p, q, c, result)
    

if __name__ == "__main__":
    logger.info("Strarting simulation.")
    if len(sys.argv) != 5:
        raise ValueError
    else:
        if sys.argv[4] == '1':
            INIT_C = INIT_C1
        else:
            INIT_C = INIT_C2
        logger.info(f"Running for c = {INIT_C}")
        for c in INIT_C:
            logger.info(f"For c = {c}")
            pyth_wrapper(
                N=int(sys.argv[1]),
                p=float(sys.argv[2]),
                q=int(sys.argv[3]),
                avg_d=14,
                c=c
            )
