import sys
import networkx as nx
import pickle
import numpy as np

SIZE = [1000, 10000, 100000]
AVG_K = [5, 10, 20]
NAMES = ["ws", "random", "ba"]

def get_graph(name: str, N, k):
    """
    
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
    graphs = [
        "ws",
        "random",
        "ba"
    ]

    L = int(k/2)
    p = k/(N-1)

    methods = dict(
        ws=nx.watts_strogatz_graph(N,k,0.01),
        random=nx.gnp_random_graph(N,p),
        ba=nx.barabasi_albert_graph(N,L)
    )
    if name.lower() not in graphs:
        raise ValueError("{} grpah is not supported".format(name))

    return methods.get(name)

def remove_nodes(G, fraction):
    to_remove = int(G.number_of_nodes() * fraction)
    # print(f"I will remove {to_remove} nodes")
    # print(f"Before: {G.number_of_nodes()}")
    for _ in range(to_remove):
        G.remove_node(
            np.random.choice(list(G.nodes()))
        )
    # print(f"After: {G.number_of_nodes()}")

def calc_avg_deg(G):
    degs = G.degree
    N = len(degs)
    return (sum([d for _, d in degs]) / N)

def calc_prob(G, n):
    bc_size = len(max(nx.connected_components(G), key=len))
    return bc_size / n

def simulate(name, N, k, f, realziations=10):
    print(f"{name}, {N}, {k}, {f} x {realziations}")
    avg_prob = 0
    for _ in range(realziations):
        G = get_graph(name, N, k)
        remove_nodes(G, f)
        avg_prob += calc_prob(G, N)
    return avg_prob/realziations

def write_result(name, N, k, data):
    with open(f"results_{name}_{N}_{k}", "wb+") as f:
        pickle.dump(data, f)
        
def main(n):
    for name in [n]:
        for N in SIZE:
            for k in AVG_K:
                fs = list()
                for f in np.linspace(0.0, 0.99, 10):
                    fs.append(simulate(name, N, k, f))
                fs = list(map(lambda x: x/fs[0], fs))
                write_result(name, N, k, fs)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ImportError("please provide the name of the graph")
    else:
        print(sys.argv[1])
        main(sys.argv[1])