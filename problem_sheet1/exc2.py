import requests
import pprint
from bs4 import BeautifulSoup
import networkx as nx
import pandas as pd
from itertools import combinations
import plotly.graph_objects as go


def main():
    phy_authors = get_phy_authors()
    unique_authors = set()
    for a in phy_authors:
        for b in a:
            unique_authors.add(b)
    g_big = create_graph(phy_authors, unique_authors)
    draw_graph(g_big, display_text=False)
    # people_phy = get_phy_data()
    # people_cs = get_cs_data()
    # authors = get_scopus_authors()
    # g_cs = create_graph(authors, people_cs)
    # g_phy = create_graph(authors, people_phy)
    # draw_graph(g_cs)
    # draw_graph(g_phy)

def create_graph(author_list, node_list):
    G = nx.Graph()
    G.add_nodes_from(node_list)
    for authors in author_list:
        cand = [author for author in authors if author in node_list]
        if len(cand) > 1:
            for v1, v2 in combinations(cand, 2):
                G.add_edge(v1,v2)

    return G
            
def get_scopus_authors():
    scopus_df = pd.read_csv("data/scopus.csv")
    scopus_authors = scopus_df['Authors']

    def format_scopus(x):
        return list(
            filter(
                lambda x: len(x) > 1,
                [name.replace(",", "").strip() for name in x.split(".")]
            )
        )
    formated_scopus = scopus_authors.map(format_scopus)
    return formated_scopus

def get_cs_data():
    r = requests.get("https://cs.pwr.edu.pl/kadraLista.php")
    soup = BeautifulSoup(r.text, "html.parser")
    tags = soup.find("tbody").find_all("tr")
    names = set()
    for t in tags:
        row = t.find_all("td")
        names.add(row[1].text.split(" ")[1] + " " + row[1].text.split(" ")[0][:1])

    return names

def get_phy_data():
    def is_valid_td(tag):
        forbidden_class = ['www', 'mail', 'office', 'phone', 'supervisor']
        if tag.name == "td":
            if "class" in tag.attrs.keys():
                return not any([f in tag['class'] for f in forbidden_class])
            return True
        return False
    abr  = ["prof.", "dr", "hab.", "inż.", "mgr", "doc."]
    r = requests.get("http://www.kft.pwr.edu.pl/?People")
    soup = BeautifulSoup(r.text, "html.parser")
    tags = soup.find_all("table", attrs={'class': 'people'})
    valid_names = set()
    manual = set()
    for t in tags:
        rows = t.find_all(is_valid_td)
        for t2 in rows:
            if t2.em:
                t2.em.extract()
            name  = " ".join([w for w in t2.text.split(" ") if w not in abr])
            if len(name.split(" ")) != 2:
                manual.add(name)
            else:
                surn = name.split(" ")[1]
                name_abr = name.split(" ")[0][:1]
                valid_names.add(f"{surn} {name_abr}")

    # print("Manual correct names:")
    # for n in manual:
    #     print(n)

    manual = set([
        "Dubowski J",
        "Mituś A",
        "Sitek A",
        "Machnikowski P",
        "Nouri N",
        "Wójs A",
        "Chmiel A",
    ])
    return valid_names | manual

def draw_graph(
    g,
    display_text=True,
    layout=nx.fruchterman_reingold_layout,
    node_size_scale=0.45
):
    pos = layout(g)

    Xed = []
    Yed = []
    for edge in g.edges():
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]

    edge_trace=go.Scatter(
        x=Xed,
        y=Yed,
        mode='lines',
        line=dict(color='rgb(210,210,210)', width=1),
        hoverinfo='none'
    )

    node_trace = go.Scatter(
        x=[pos[node][0] for node in g.nodes()],
        y=[pos[node][1] for node in g.nodes()],
        mode="markers+text",
        hoverinfo="text",
        hovertext=[],
        text = [node for node in g.nodes()] if display_text else [],
        textposition="top center",
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=False,
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
    degree = []
    for adjacencies in g.adjacency():
        degree.append(len(adjacencies[1]))

    node_trace.marker.size = [8 + node_size_scale*deg for deg in degree]
    node_trace.hovertext = degree if display_text else [f"{n[0]}: {len(n[1])}" for n in g.adjacency()]
    node_trace.marker.color = degree

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

def get_scopus_data():
    key = {'apiKey': '8912a6d3788c9ffb6fcc79bdd1adb536'}
    address = "https://api.elsevier.com/content/search/scopus"
    r = requests.get(
        address,
        headers={
            'Accept':'application/json',
            'X-ELS-APIKey': key['apiKey'] 
        },
        params={
            'query':'Wrocław University of Science and Technology',
            # 'field':'url,identifier,description'
            'count': '25'
        }
    )
    print(r.status_code)

    print(r.headers['content-type'])

    print(r.encoding)

    pprint.pprint(r.json())
    test = [(e['dc:creator'], [a['affilname'] for a in e['affiliation']]) for e in r.json()['search-results']['entry']]

    r = requests.get(
        address,
        headers={
            'Accept':'application/json',
            'X-ELS-APIKey': key['apiKey'] 
        },
        params={
            'query':'Wrocław University of Science and Technology',
            # 'field':'url,identifier,description'
            'start': '25',
            'count': '25'
        }
    )
    test.extend(
        [(e['dc:creator'], [a['affilname'] for a in e['affiliation']]) for e in r.json()['search-results']['entry']])
    for i in test:
        print(i)

def get_phy_authors():
    def clear_li(tag):
        return tag.name =="li" and not tag.has_attr("class")
    r = requests.get("http://www.kft.pwr.edu.pl/?Publications")
    soup = BeautifulSoup(r.text, "html.parser")
    lists = soup.find_all("ul")
    authors = []
    for l in lists:
        items = l.find_all(clear_li)
        for i in items:
            authors.append([name.strip() for name in str(i).split("<em>")[0][4:].split(",") if len(name) > 1])

    return authors

if __name__ == "__main__":
    main()