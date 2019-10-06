import plotly.graph_objects as go

import networkx as nx

G = nx.random_geometric_graph(5, 0.5)
print(G.edges())
print(G.node[0])

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_y.append(y0)
    edge_y.append(y1)

print(edge_x)
print(edge_y)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_trace = go.Scatter(
    x=[ G.node[node]['pos'][0] for node in G.nodes()],
    y=[ G.node[node]['pos'][1] for node in G.nodes()],
    mode='markers',
    text=[str(x) for x in range(len(G.nodes()))],
    marker=dict(
        showscale=True,
        colorscale='Electric'
    )
)

fig = go.Figure(
    data=[edge_trace, node_trace]
)
fig.show()