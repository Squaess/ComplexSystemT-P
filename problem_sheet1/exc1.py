import plotly.graph_objects as go
import networkx as nx
import os

# create graph from file which is in gml format
g = nx.readwrite.gml.read_gml("data/dolphins/dolphins.gml")

# generate x and y position for all nodes
# this is needed for drawing
pos = nx.fruchterman_reingold_layout(g)

# vertex postions
Xv = [pos[k][0] for k in g.nodes()]
Yv = [pos[k][1] for k in g.nodes()]

# Edges prositions in format: 
# [start, end, None, start2, end2, None, ...]
Xed = []
Yed = []
for edge in g.edges():
    Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
    Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]

# edge trace
edge_trace=go.Scatter(
    x=Xed,
    y=Yed,
    mode='lines',
    line=dict(color='rgb(210,210,210)', width=1),
    hoverinfo='none'
)

# node trace
node_trace=go.Scatter(
    x=Xv,
    y=Yv,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right',
        ),
        line_width=2
    ),
)

# list of degrees
# for each node
node_adjacencies = []

# container for the hover text 
# for each node
node_text = []
for node, adjacencies in enumerate(g.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append(
        '{}: {}'.format(
            adjacencies[0],
            len(adjacencies[1])
        )
    )

# make color propotional to the
# node degree
node_trace.marker.color=node_adjacencies
node_trace.text = node_text

# Figure objec: this will be displayd
fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title="<br>Dolphins connections.<br>",
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=45),
        annotations=[ dict(
            text="Python code: <a href=''>Python code on Github.</a>",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002 ) ],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
)
fig.show()

# save file in case of not working browser
node_trace.mode="markers+text"
if not os.path.exists("results"):
    os.mkdir("results")

fig.write_image("results/exc1.png")