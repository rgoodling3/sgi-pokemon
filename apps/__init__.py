
import plotly.graph_objects as go
import networkx as nx
from pokemon_episodes_graph import generate_generation_graph, get_generations_dict
from location_graph import generate_games_graph, get_game_dict
import pandas as pd


def random_graph(no_nodes=200, edge_percent=0.125):
    return nx.random_geometric_graph(no_nodes, edge_percent)


def create_edge_trace(G):
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    a = []
    b = []
    for i, edge in enumerate(G.edges()):
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        a.append(x0)
        a.append(x1)
        a.append(None)
        b.append(y0)
        b.append(y1)
        b.append(None)
        # edge_trace['x']+=(x_tuple)
        # edge_trace['y']+=(y_tuple)
    edge_trace['x'] = tuple(a)
    edge_trace['y'] = tuple(b)
    return edge_trace


def create_node_trace(G, include_bar=True):
    if include_bar is True:
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
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
                    titleside='right'
                ),
                line=dict(width=2)))
    else:
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text'
        )
    for i, node in enumerate(G.nodes()):
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    return node_trace


def add_color_and_hover_text(G, node_trace):
    # add color to node points
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: ' + str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])


def create_figure(node_trace, edge_trace):
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            height=1000,
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            # xaxis=dict(range=[0, 1]),
            # yaxis=dict(range=[0, 1])
        )
    )
    return fig


def get_graph_figure(gen_number):
    generations = get_generations_dict()
    G = generate_generation_graph(generations[gen_number])
    positions = nx.random_layout(G)
    # for item in positions.values():
    # item[0] *= 5
    # item[1] *= 5
    nx.set_node_attributes(G, positions, 'pos')
    node_trace = create_node_trace(G)
    edge_trace = create_edge_trace(G)
    add_color_and_hover_text(G, node_trace)
    fig = create_figure(node_trace, edge_trace)

    return G, fig


seasons = get_generations_dict()
'''
graphs = []
figures = []
for i in range(len(seasons)):
    g, f = get_graph_figure(i + 1)
    graphs.append(g)
    figures.append(f)
'''

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowY': 'scroll',
        'fontSize': '20px',
        'height': '350px'
    },
    'img': {
        'padding': '15px',
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'width': '75%',
        'display': 'block'
    },
    'centeredMarkdown': {
        'textAlign': 'center',
    }
}

def route_get_graph_figure(game):
    games = get_game_dict()
    G, color_map = generate_games_graph(games[game])
    positions = nx.random_layout(G)
    nx.set_node_attributes(G, positions, 'pos')
    node_trace = create_node_trace(G, False)
    edge_trace = create_edge_trace(G)
    node_trace['marker']['color'] = color_map
    routes_add_color_and_hover_text(G, node_trace)
    fig = create_figure(node_trace, edge_trace)

    return G, fig


def routes_add_color_and_hover_text(G, node_trace):
    # add color to node points
    node_trace['text'] = list(G.nodes())
    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(5 * len(adjacencies[1]))
    node_trace["marker"]['size'] = node_adjacencies
    node_trace["marker"]['colorbar'] = None


def small_graph (game, clickData):
    markercolor = clickData['points'][0]['marker.color']
    name = clickData['points'][0]['text']
    g, f = route_get_graph_figure(game)
    G = nx.Graph()
    G.add_edges_from(g.edges(name))
    positions = nx.random_layout(G)
    nx.set_node_attributes(G, positions, 'pos')
    color_map = []
    node_adjacencies = []
    adjDict = dict(route_graphs[game].adjacency())
    for x in G.nodes():
        if x == name:
            color_map.append(markercolor)
        else:
            if markercolor == 'rgb(0,240,0)':
                color_map.append('rgb(192, 143, 227)')
            else:
                color_map.append('rgb(0,240,0)')
        if x in adjDict:
            node_adjacencies.append(2 * len(adjDict[x]))
    node_trace = create_node_trace(G, False)
    node_trace['marker']['color'] = color_map
    node_trace["marker"]['size'] = node_adjacencies
    node_trace['text'] = list(G.nodes())
    fig = create_figure(node_trace, create_edge_trace(G))
    fig.layout["height"] = 400
    return fig

games = get_game_dict()
route_graphs = []
route_figures = []
for i in range(len(games)):
    g, f = route_get_graph_figure(i + 1)
    route_graphs.append(g)
    route_figures.append(f)

df = pd.read_csv("./pokemon_data.csv")