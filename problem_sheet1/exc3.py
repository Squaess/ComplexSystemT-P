from nltk.tokenize import RegexpTokenizer
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import numpy as np
import networkx as nx
from exc2 import draw_graph

def read_stopword() -> list:
    """Read polish stopwords from file
    
    Returns:
        list: list of polish stopwords
    """
    stopwords = None
    with open("data/stopwords_pl.txt", "r", encoding="utf-8") as f:
        stopwords =  f.read().split("\n")
    return stopwords

stopwords = read_stopword()
book = None

# read the book and split using tokenizer
t = RegexpTokenizer(r"\w+")
with open("data/book.txt", "r", encoding="utf-8") as f:
    book = t.tokenize(f.read())

# clean book, filter stopwords parse all to lowercase
cleaned_book = [w.lower() for w in book if w not in stopwords]

# create frequency rank
rank = dict()
for w in cleaned_book:
    if w in rank:
        rank[w] += 1
    else:
        rank[w] = 1

# sort rank items by second value which is frequency
rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)

# create domain
X = np.arange(1,len(rank)+1)
# get frequency values
Y = np.array([value for _, value in rank])

#p lot
fig = go.Figure(
    data=go.Scatter(
        x=X,
        y=Y,
        mode="lines"
    ),
    layout=go.Layout(
        title="Frequency - rank dependence, normal scale"
    )
)
fig.show()

# display in log scale
fig.update_layout(xaxis_type="log", yaxis_type="log", title="Frequency - rank dependency, log scale")
fig.show()

# Get log data from source
X_log = np.log(X)
Y_log = np.log(Y)

# create linear regression model for log data
slope, intercept, r_value, p_value, std_err = stats.linregress(
    X_log,
    Y_log
)

# get points for linear regression model
line = slope * X_log + intercept

# reg model line
trace1 = go.Scatter(
    x=X_log,
    y=line,
    mode="lines",
    name="lin. regression model: coef - a:{}, b:{}".format(slope, intercept)
)

# logY "line"
trace2 = go.Scatter(
    x=X_log,
    y=Y_log,
    mode="lines",
    name="frequency data"
)
fig = go.Figure(
    data=[trace1, trace2], 
    layout=go.Layout(
        title="Frequency - rank dependence with liner regression model.",
        plot_bgcolor='rgb(229,229,229)',
    )
)
fig.show()

# create graph and add edges
G = nx.Graph()
for i in range(1,len(cleaned_book)):
    source = cleaned_book[i-1]
    target = cleaned_book[i]
    G.add_edge(source, target)

# sort nodes by degree
word_adj = sorted(G.degree(), key=lambda x: x[1], reverse=True)
print("Top 10 degrees:")
for i in word_adj[:10]:
    print(i)

print("Worst 10 degrees:")
for i in word_adj[:-10:-1]:
    print(i)


# ploting all nodes with fruchterman_reginold_layout is almost impossible
# calculations of position takes too long and the graph is unreadable

# create subplot with nodes that degree > 10
g = nx.subgraph(G, [node for node, deg in word_adj if deg > 10])
draw_graph(g, display_text=False, node_size_scale=0.2, title="Word adjacency netowrk.")

# create pandas df for simplicity of plotly
nodes_df = pd.DataFrame([[node, deg] for node, deg in G.degree()])

# plot histogram of nodes
fig = px.histogram(
    nodes_df,
    x=1,
    hover_data=nodes_df.columns,
)
fig.update_xaxes(
    title_text="Word adjacency histogram"
)
fig.show()