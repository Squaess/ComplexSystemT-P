import os
import requests
import pprint
from bs4 import BeautifulSoup
import networkx as nx
import pandas as pd
from itertools import combinations
import plotly.graph_objects as go


def main():
    """Main function
    """
    # scopus data

    # get physics department workers
    people_phy = get_phy_data()

    # get cs department workers
    people_cs = get_cs_data()

    # get list of collaborative authors
    # from scopus
    authors = get_scopus_authors()

    # create needed graphs
    g_cs = create_graph(authors, people_cs)
    g_phy = create_graph(authors, people_phy)

    # draw graphs
    draw_graph(g_cs, save=True, save_name="graph_cs.png")
    draw_graph(g_phy, save=True, save_name="graph_phy.png")

    # kft data
    phy_authors = get_phy_authors()
    # get list of nodes
    unique_authors = set()
    for a in phy_authors:
        for b in a:
            unique_authors.add(b)
    g_big = create_graph(phy_authors, unique_authors)
    draw_graph(g_big, display_text=False, save=True, save_name="graph_kft.png")

def create_graph(author_list: list, node_list: list) -> nx.Graph:
    """Creates undirected graph of author collaboration.
    
    Args:
        author_list (list): list of lists of author collaboration
        node_list (list): list of authors that will be taken under consideration
    
    Returns:
        nx.Graph: graph of collaboration
    """
    # create graph
    G = nx.Graph()

    # add nodes
    G.add_nodes_from(node_list)

    for authors in author_list:
        # get only important authors
        cand = [author for author in authors if author in node_list]
        if len(cand) > 1:
            # if more than 1 author create edges
            for v1, v2 in combinations(cand, 2):
                G.add_edge(v1,v2)

    return G
            
def get_scopus_authors() -> list:
    """Extract needed values from the csv file.
    
    Returns:
        list: List of list, author collaborations:
            [[a1, a2], [a2, a3, a4],  ...]
    """

    # read csv file
    scopus_df = pd.read_csv("data/scopus.csv")

    # get only Authors column
    scopus_authors = scopus_df['Authors']

    def format_scopus(x: str) -> list:
        """Clean and format scopus author data.
        
        Args:
            x (str): One cell of data
        
        Returns:
            list: list of names properly formated.
        """
        return list(
            filter(
                lambda x: len(x) > 1,  # need to be at least name and surname 
                                       # if multiple names then just one will be used
                [name.replace(",", "").strip() for name in x.split(".")]
            )
        )
    formated_scopus = scopus_authors.map(format_scopus)
    return formated_scopus

def get_cs_data() -> set:
    """Get workers from cs department
    
    Returns:
        set: set that contains all workers
    """
    # get site
    r = requests.get("https://cs.pwr.edu.pl/kadraLista.php")

    # parse site
    soup = BeautifulSoup(r.text, "html.parser")
    tags = soup.find("tbody").find_all("tr")
    names = set()
    for t in tags:
        row = t.find_all("td")
        # add to names properly formated string
        names.add(row[1].text.split(" ")[1] + " " + row[1].text.split(" ")[0][:1])

    return names

def get_phy_data() -> set:
    """Gets workers from http://www.kft.pwr.edu.pl/?People.
    
    Returns:
        set: set of workers
    """
    def is_valid_td(tag):
        """Check for needed tag.
        
        Args:
            tag (bs4.element.Tag): Tag element
        
        Returns:
            bool: If the tag match the criteria
        """
        forbidden_class = ['www', 'mail', 'office', 'phone', 'supervisor']
        if tag.name == "td":
            if "class" in tag.attrs.keys():
                return not any([f in tag['class'] for f in forbidden_class])
            return True
        return False
    
    # list of scientific abbreviations
    # that will be removed when cleaning data
    abr  = ["prof.", "dr", "hab.", "inż.", "mgr", "doc."]

    # get site content
    r = requests.get("http://www.kft.pwr.edu.pl/?People")

    #parse the site content
    soup = BeautifulSoup(r.text, "html.parser")
    tags = soup.find_all("table", attrs={'class': 'people'})

    # valid names is the set
    # which names where properly parsed
    valid_names = set()

    # manual is is set where something
    # went wrong need to display and 
    # fix manually
    manual = set()
    for t in tags:
        rows = t.find_all(is_valid_td)
        for t2 in rows:
            # remove <em> tag and content from element
            if t2.em:
                t2.em.extract()
            # create name without scienctific abbrevation
            name  = " ".join([w for w in t2.text.split(" ") if w not in abr])
            if len(name.split(" ")) != 2:
                manual.add(name)
            else:
                # if the format is ok then parse it to
                # Surname N instead of Name Surname
                surn = name.split(" ")[1]
                name_abr = name.split(" ")[0][:1]
                valid_names.add(f"{surn} {name_abr}")

    # print manual values to cerrect below
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
        title="Collaboration network.",
        display_text=True,
        layout=nx.fruchterman_reingold_layout,
        node_size_scale=0.45,
        save=False,
        save_name="result.png"
    ):
    """Function used for drawing social graphs.
    Quite generic function can be reused.

    Args:
        g (nx.Graph): Graph object
        titile (str, optional): Figure titile if needed to change. Defaults to 'Collaboration network.'
        display_text (bool, optional): Whether to display node text under the nodes. Defaults to True.
        layout (nx.drawing.layout(function), optional): Type of layout to be used. Defaults to nx.fruchterman_reingold_layout.
        node_size_scale (float, optional): Node size scaling factor. Defaults to 0.45.
        save (bool, optional): Whether to save graph in png. Defaults to False.
        save_name (str, optional): Name of the png file that will be saved if save=True

    Returns:
        None: None
    """
    # extended version of algorithm from exc1.py
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
            title=f"<br>{title}<br>",
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

    if save:
        if not os.path.exists("results"):
            os.mkdir("results")
        fig.write_image("results/"+save_name)

def get_phy_authors() -> list:
    """Function that fetch publication data
    stored on http://www.kft.pwr.edu.pl/?Publications
    and parse authors.
    
    Returns:
        list: List containing list of authors that 
            were collaborating on the same paper.
            [[author1, author2], [author2, author3, author4], ...]
    """
    def clear_li(tag):
        """Function used to get only neede tag when
        parsing kft site.
        
        Args:
            tag (bs4.element.Tag): tag element
        
        Returns:
            bool: if the tag is valid or not
        """
        return tag.name =="li" and not tag.has_attr("class")

    # get the whole site and parse using bs4
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