"""
Most of the code is the same as in previos list, there's
just a difference in removing the nodes.
"""
import sys
import os
import pickle
import logging
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

SIZES = [100, 1000, 10000]
# SIZES = [50, 100]#, 1000]
# SIZES = [1000]
AVG_K = [5, 10, 20]
REALIZATIONS = 10

def get_graph(name: str, N, k) -> nx.Graph:
    """ returns given graphs with average <k>
    
    Args:
        name (str): Type of graph to return
        N (int): number of nodes
        k (int): average degree

    Raises:
        ValueError: when given graph typer is not supported

    Returns:
        nx.Graph: desired graph
    """
    name = name.lower()
    names = [
        "ws",
        "random",
        "ba"
    ]
    if name not in names:
        raise ValueError()

    # values needed for random graph and
    # watts strogatz graph
    L = int(k/2)
    p = k/(N-1)

    if name == "ws":
        return nx.watts_strogatz_graph(N,k,0.01)
    if name == "ba":
        return nx.barabasi_albert_graph(N,L)
    if name == "random":
        return nx.fast_gnp_random_graph(N,p)

def remove_cc(G: nx.Graph, n: int, f: float):
    """ Remove using closeness_centrality
    """
    to_remove = int(n * f)
    cc = nx.algorithms.closeness_centrality(G)
    nn_remove = [i for i,_ in sorted(cc.items(), key=lambda x: x[1], reverse=True)[:to_remove]]
    G.remove_nodes_from(nn_remove)

def remove_bc(G: nx.Graph, n: int, f: float):
    """ Remove usgin betweenness_centrality
    """
    to_remove = int(n * f)
    cc = nx.algorithms.betweenness_centrality(G)
    nn_remove = [i for i,_ in sorted(cc.items(), key=lambda x: x[1], reverse=True)[:to_remove]]
    G.remove_nodes_from(nn_remove)
    
def remove_nodes(G: nx.Graph, n: int, f: float, kind: str):
    logger.info(f"Removing {f} fraction of nodes using {kind} method")
    if kind == "cc":
        return remove_cc(G, n, f)
    if kind == "bc":
        return remove_bc(G, n, f)

def calc_prob(G, n):
    bc_size = len(max(nx.connected_components(G), key=len))
    return bc_size/n

def write_result(name:str, n:int, k:int, x:list, y:list, kind:str):
    path = f"results"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+f"/{name}_{kind}_{n}_{k}", "wb+") as f:
        pickle.dump(zip(x, y), f)
    
def main(name: str, kind: str):
    kind_choice = ["cc", "bc"]
    if kind not in kind_choice:
        raise ValueError("Wrong method of removing nodes.")
    fractions = np.linspace(0.0, 0.99, 10)
    for n in SIZES:
        for k in AVG_K:
            fs = []
            for f in fractions:
                logger.info(f"Calculating {name} = N:{n}, k:{k}, {f} ... ")
                logger.info(f"With {REALIZATIONS} indep, realizations.")
                avg_f = 0
                for ix in range(REALIZATIONS):
                    logger.info(f"Gen graph N={n}, it={ix}")
                    G = get_graph(name, n, k)
                    remove_nodes(G, n, f, kind)
                    avg_f += calc_prob(G, n)
                avg_f = avg_f/REALIZATIONS
                fs.append(avg_f)
            fs = list(map(lambda x: x/fs[0], fs))
            write_result(name, n, k, fractions, fs, kind)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("We need just one parameter for the name.")
    else:
        # main(sys.argv[1], "cc")
        main(sys.argv[1], "bc")
