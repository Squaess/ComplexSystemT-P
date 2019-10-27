from nltk.tokenize import RegexpTokenizer
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import numpy as np
import networkx as nx
from exc2 import draw_graph

def read_stopword():
    stopwords = None
    with open("data/stopwords_pl.txt", "r", encoding="utf-8") as f:
        stopwords =  f.read().split("\n")
    return stopwords

stopwords = read_stopword()
book = None
t = RegexpTokenizer(r"\w+")
with open("data/book.txt", "r", encoding="utf-8") as f:
    book = t.tokenize(f.read())

cleaned_book = [w.lower() for w in book if w not in stopwords]

rank = dict()
for w in cleaned_book:
    if w in rank:
        rank[w] += 1
    else:
        rank[w] = 1

rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)
X = np.arange(1,len(rank)+1)
Y = np.array([value for _, value in rank])
# fig = go.Figure(
#     data=go.Scatter(
#         x=X,
#         y=Y,
#         mode="lines"
#     )
# )
# # fig.show()

# fig.update_layout(xaxis_type="log", yaxis_type="log")
# # fig.show()

# X_log = np.log(X)
# Y_log = np.log(Y)
# slope, intercept, r_value, p_value, std_err = stats.linregress(
#     X_log,
#     Y_log
# )
# line = slope * np.log(X) + intercept
# trace1 = go.Scatter(
#     x=X_log,
#     y=line,
#     mode="lines"
# )
# trace2 = go.Scatter(
#     x=X_log,
#     y=Y_log,
#     mode="lines"
# )
# fig = go.Figure(
#     data=[trace1, trace2], 
#     layout=go.Layout(
#         title="Cośtam",
#         plot_bgcolor='rgb(229,229,229)',
#     )
# )
# fig.show()

G = nx.Graph()
print(len(cleaned_book))
for i in range(1,len(cleaned_book)):
    source = cleaned_book[i-1]
    target = cleaned_book[i]
    G.add_edge(source, target)

word_adj = sorted(G.degree(), key=lambda x: x[1], reverse=True)
print(word_adj[:10])
print(word_adj[-10:])


# print("Creating layout")
# pos = nx.drawing.layout.kamada_kawai_layout(G)
# pos = nx.fruchterman_reingold_layout(G)    
# g = nx.subgraph(G, [node for node, deg in word_adj if deg > 10])
# print(len(g.nodes()))
# print("Starting to draw the graph.")
# draw_graph(g, display_text=False, node_size_scale=0.2)

nodes_df = pd.DataFrame([[node, deg] for node, deg in G.degree()])
fig = px.histogram(nodes_df, x=1, marginal="rug", # can be `box`, `violin`
                         hover_data=nodes_df.columns)
fig.show()