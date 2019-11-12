import plotly.express as px
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


def degree_hist(G: nx.Graph, title: str) -> None:
    G_nodes = pd.DataFrame(
        [dict(node=node, degree=deg) for node, deg in G.degree()]
    )
    fig = px.histogram(
        G_nodes,
        x="degree",
        marginal="box",
        histnorm='probability density'
    )
    fig.update_layout(title=title)
    fig.show()


def clust_hist(G: nx.Graph, title: str) -> None:
    G_cc = pd.DataFrame(
        [dict(node=node, clust_coef=cc) for node, cc in nx.algorithms.clustering(G).items()]
    )
    fig = px.histogram(
        G_cc,
        x="clust_coef",
        marginal="box",
        histnorm='probability density'
    )
    fig.update_layout(title=title)
    fig.show()


def path_hist(G: nx.Graph, title, retarted=False):
    shortest_paths = nx.shortest_path_length(G)
    path_lengths = []
    for l in tqdm(shortest_paths):
        path_lengths.extend(l[1].values())

    if not retarted:
        G_sp = pd.DataFrame(
            [dict(length=length) for length in path_lengths]
        )
        fig = px.histogram(
            G_sp,
            x="length",
            marginal="box",
            histnorm='probability density'
        )
        fig.update_layout(title=title)
        fig.show()
    else:
        fig = plt.hist(path_lengths)
        plt.title(title)
        plt.show()