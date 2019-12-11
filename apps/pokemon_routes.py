import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
from . import *
from app import app, para_style, header_style_centered, para_style_centered, title_style
import dash
from . import small_graph

layout = html.Div([
    dcc.Markdown(d('**Pokemon-routes graph**'), style=title_style),
    dcc.Markdown(d("""
        Below is a graph of the locations that Pokemon are found in the games. To explore the graph, 
        you can first click on a node in the graph on top. This will show you the node and its connections in a 
        smaller graph below. You can then click on another node in either graph to continue to explore. The node's 
        name and connections will also be displayed in text form on the side.
    """), style=para_style),
    html.Div(children=[
        dcc.Graph(id='routes'),
        dcc.Slider(
            id='game-slider',
            min=1,
            max=4,
            value=1,
            marks=
            {
                key: games[key]["name"] for key in games.keys()
            },
            step=None
        )
    ], style={'paddingLeft': "50px", 'paddingRight': "50px"}),
    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown('**Selected node graph**', style=header_style_centered),
            dcc.Graph(id='smaller'),
        ], className='eight columns'),
        html.Div([
            dcc.Markdown('**Route and Pokemon Data**', style=header_style_centered),
            dcc.Markdown(d("""
                Click on a node to see the name of the route or pokemon along with the adjacent nodes.
            """), style=para_style_centered),
            html.Pre(id='display-data', style=styles['pre']),
        ], className='four columns')
    ], style={'paddingLeft': "50px", 'paddingRight': "50px"}),
    dcc.Markdown('**Analysis**', style=header_style_centered),
    dcc.Markdown(d("""
        This graph was able to show an emphasis on the Pokemon and Locations that are most popular in the games. 
        Going through each game's graph, it is clear to see that Magicarp is almost always the largest node. 
        This tells us that in the games, Magicarp can be found in the most locations. 
        Interestingly, there does not seem to be a stand out location for the games that you can find a 
        large amount of Pokemon at. With this graph, we were hoping to see if there were some locations that you 
        could go to in order to collect a majority of Pokemon in a game. That does not seem to be the case, as 
        the average degree distribution for location nodes is 4-5 depending on the game. Having this graph be 
        structured as a bipartite graph helped with this analysis. 
        
        We also can see that Pokemon don't always group up in similar locations in the games. 
        We hypothesized that certain locations would have extremely 
        similar nodes, but in fact that is not the case. Most locations have a diverse variety of Pokemon appearing 
        there. We expected things like water types to be found by most locations containing water, but that ended up 
        not being the case. The locations containing water will typically include water types, but the combination of 
        the Pokemon will still vary from location to location. 

        Tools that were used to help find this analysis were bipartite graph and community detection.
    """), style=para_style)
])


@app.callback(
    Output('routes', 'figure'),
    [Input('game-slider', 'value')])
def update_figure(game):
    return route_figures[game - 1]


@app.callback(
    Output('smaller', 'figure'),
    [Input('routes', 'clickData'), Input('game-slider', 'value'), Input('smaller', 'clickData')])
def display_click_data(clickData, game, smallClick):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    elif ctx.triggered[0]['prop_id'] == 'routes.clickData':
        if clickData is not None:
            fig = small_graph(game, clickData)
            return fig
    elif ctx.triggered[0]['prop_id'] == 'smaller.clickData':
        if smallClick is not None:
            fig = small_graph(game, smallClick)
            return fig
    else:
        return dash.no_update


@app.callback(
    Output('display-data', 'children'),
    [Input('routes', 'clickData'), Input('smaller', 'clickData'), Input('game-slider', 'value')])
def display_click_data(clickData, smallClick, game):
    result = ""
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    elif ctx.triggered[0]['prop_id'] == 'routes.clickData':
        if clickData is not None:
            name = clickData['points'][0]['text']
            text = "Pokemon Name" if clickData['points'][0]['marker.color'] == 'rgb(192, 143, 227)' else "Location Name"
            g = route_graphs[game - 1]
            edges = ""
            for x in g.edges(name):
                edges = edges + str(x[1]) + "\n     "
            result = f"""
{text}: {name}
Connected to:\n     {edges}
                """
        return result
    elif ctx.triggered[0]['prop_id'] == 'smaller.clickData':
        if smallClick is not None:
            name = smallClick['points'][0]['text']
            text = "Pokemon Name" if clickData['points'][0]['marker.color'] == 'rgb(192, 143, 227)' else "Location Name"
            g = route_graphs[game - 1]
            edges = ""
            for x in g.edges(name):
                edges = edges + str(x[1]) + "\n     "
            result = f"""
{text}: {name}
Connected to:\n     {edges}
                """
        return result