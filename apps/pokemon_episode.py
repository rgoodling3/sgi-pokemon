import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import re
from . import *
from app import app, para_style, para_style_centered, title_style, header_style_centered
import base64

image_filename = './community-graphs/community_gen1.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

distribution_img = './distributions/degree_dist1.png'
encoded_dist = base64.b64encode(open(distribution_img, 'rb').read())

layout = html.Div([
    dcc.Markdown("**Pokemon-episode graph**", style=title_style),
    dcc.Markdown(d("""
        This section shows 7 graphs, each corresponding to one of the seven seasons of Pokemon anime.        
        The nodes marked with the brightest color represents the pokemon who met the most of other pokemons throughout 
        their appearance in the season episodes 
        
        Use a slider to switch between the graphs. 
        
        **NOTE** due to the limitations of response time of used cloud 
        hosting service, the graphs are generated after the slider action is performed. Hence, please wait 5-10sec
        for a graph to load.
    """), style=para_style),
    html.Div(children=[
        dcc.Graph(id='Graph'),
        dcc.Slider(
                 id='season-slider',
                 min=1, max=7, value=1,
                 marks={key: seasons[key]["name"] for key in seasons.keys()},
                 step=None
        )
        ],
        style={'paddingLeft': "50px", 'paddingRight': "50px"}),
    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown('**Click Data**', style=header_style_centered),
            dcc.Markdown(d("""        
            Click on nodes in the graph to display information about the Pokemon.
        """), style=para_style_centered),
            html.Pre(id='click-data', style=styles['pre']),

        ], className='four columns'),
        html.Div([
            dcc.Markdown('**Click Data Image**', style=header_style_centered),
            dcc.Markdown(d("""
                Displays image of the clicked node's Pokemon
            """), style=para_style_centered),
            html.Img(id='image', src="https://pbs.twimg.com/profile_images/677508993686700035/5hQ59Dm4_400x400.png", style=styles['img'])
        ], className='four columns'),
        html.Div([
            dcc.Markdown('**Selection Data**', style=header_style_centered),
            dcc.Markdown(d("""                
                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.
            """), style=para_style_centered),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='four columns')
    ],
             style={'paddingTop': '50px', 'paddingLeft': '100px', 'paddingRight': '100px'}),

    dcc.Markdown("**Community detection for the various generations**", style=title_style),
    html.Div(children=[
        html.Div(className='row', children=[
                html.Div(className='three columns', children=
                         html.Img(id='community-graph',  src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '70vw'})),

                html.Div(className='three columns'),
                html.Div(className='three columns'),
                html.Div(className='three columns', children=[
                    dcc.Markdown(id='community-info', children=f'''
                    ## Community info:
                    #### Number of communities: 7
                    #### Modularity of the network: 0.09375
                    #### Community label: 0. Number of pokemons in community: 31 out of 154
        
                    #### Community label: 1. Number of pokemons in community: 47 out of 154
        
                    #### Community label: 2. Number of pokemons in community: 23 out of 154
        
                    #### Community label: 3. Number of pokemons in community: 50 out of 154
        
                    #### Community label: 4. Number of pokemons in community: 1 out of 154
        
                    #### Community label: 5. Number of pokemons in community: 1 out of 154
        
                    #### Community label: 6. Number of pokemons in community: 1 out of 154         
                    ''', style={'paddingTop': '25vh', 'paddingRight': '10vw'})
                ])
            ]),
        dcc.Slider(
                id='community-slider',
                min=1,
                max=7,
                value=1,
                marks={1: 'The Beginning', 2: 'Gold & Silver', 3: 'Ruby & Sapphire', 4: 'Diamond & Pearl', 5: 'Black & White',
                       6: 'X & Y', 7: 'Sun & Moon'}
            ),
    ], style={'paddingLeft': "50px", 'paddingRight': "50px"}),
    html.Hr(),
    dcc.Markdown("**Degree distributions and various network statistics**", style=title_style),
    html.Div(children=[
        html.Div(className='row', children=[
                html.Div(className='three columns', children=
                html.Img(id='distribution-img', src='data:image/png;base64,{}'.format(encoded_dist.decode()),
                         style={'width': '70vw'})),

                html.Div(className='three columns'),
                html.Div(className='three columns'),
                html.Div(className='three columns', children=[
                    dcc.Markdown(id='statistics-info', children=f'''
                # Network statistics:
                #### Number of nodes: 7
                #### Number of edges: 0.09375
                #### Average degree: bla
                #### Average shortest path: bla
                #### Global clustering coefficient: bla
                #### Assortativity coefficient: bla       
                #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free 
                ''', style={'paddingTop': '25vh', 'paddingRight': '10vw'})
                ])
            ]),
        dcc.Slider(
            id='statistics-slider',
            min=1,
            max=7,
            value=1,
            marks={1: 'The Beginning', 2: 'Gold & Silver', 3: 'Ruby & Sapphire', 4: 'Diamond & Pearl', 5: 'Black & White',
                   6: 'X & Y', 7: 'Sun & Moon'}
        )
    ], style={'paddingTop': '50px', 'paddingLeft': '100px', 'paddingRight': '100px'})

])

@app.callback(
    Output('Graph', 'figure'),
    [Input('season-slider', 'value')])
def update_figure(selected_season):
    _, fig = get_graph_figure(selected_season)
    return fig
    #return figures[selected_season - 1]


@app.callback(
    Output('image', 'src'),
    [Input('Graph', 'clickData')]
)
def display_img(clickData):
    if clickData is not None:
        text = clickData["points"][0]["text"]
        name = re.search(r"(?<=Name: )(.*)(?=<br>)", text)[0]
        url = f"https://img.pokemondb.net/artwork/{name.lower()}.jpg"
    else:
        url = 'https://pbs.twimg.com/profile_images/677508993686700035/5hQ59Dm4_400x400.png'
    return url


@app.callback(
    Output('click-data', 'children'),
    [Input('Graph', 'clickData')])
def display_click_data(clickData):
    result = ""
    if clickData is not None:
        text = clickData["points"][0]["text"]
        name = re.search(r"(?<=Name: )(.*)(?=<br>)", text)[0]
        sentiment = df[df["Pokémon"] == name]["Sentiment_stemmed"].values[0]
        generation = df[df["Pokémon"] == name]["Generation"].values[0]
        type = df[df["Pokémon"] == name]["Type"].values[0]
        result = f"""
Name: {name}
  Type: {type}
  Generation: {generation}
  Sentiment: {sentiment}
        """

        # no_connections = re.search(r"(?<=connections: )(.*)", text)[0]
    # return json.dumps(clickData, indent=2)
    return result


@app.callback(
    Output('selected-data', 'children'),
    [Input('Graph', 'selectedData')])
def display_selected_data(selectedData):
    result = ""
    if selectedData is not None:
        for point in selectedData["points"]:
            text = point["text"]
            name = re.search(r"(?<=Name: )(.*)(?=<br>)", text)[0]
            sentiment = df[df["Pokémon"] == name]["Sentiment_stemmed"].values[0]
            generation = df[df["Pokémon"] == name]["Generation"].values[0]
            type = df[df["Pokémon"] == name]["Type"].values[0]
            result += f"""
Name: {name}
  Type: {type}
  Generation: {generation}
  Sentiment: {sentiment}
            """

    return result


@app.callback(
    [Output('community-graph', 'src'),
     Output('community-info', 'children')],
    [Input('community-slider', 'value')]
)
def update_community(generation):
    image_filename = f'./community-graphs/community_gen{generation}.png'  # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    if generation == 1:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
            ## Community info:
            #### Number of communities: 7
            #### Modularity of the network: 0.09375
            #### Community label: 0. Number of pokemons in community: 31 out of 154

            #### Community label: 1. Number of pokemons in community: 47 out of 154

            #### Community label: 2. Number of pokemons in community: 23 out of 154

            #### Community label: 3. Number of pokemons in community: 50 out of 154

            #### Community label: 4. Number of pokemons in community: 1 out of 154

            #### Community label: 5. Number of pokemons in community: 1 out of 154

            #### Community label: 6. Number of pokemons in community: 1 out of 154         
            '''
    elif generation == 2:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
             ## Community info:
             #### Number of communities: 10
             #### Modularity of the network: 0.12437
             #### Community label: 0. Number of pokemons in community: 22 out of 258

             #### Community label: 1. Number of pokemons in community: 85 out of 258

             #### Community label: 2. Number of pokemons in community: 1 out of 258

             #### Community label: 3. Number of pokemons in community: 45 out of 258

             #### Community label: 4. Number of pokemons in community: 67 out of 258

             #### Community label: 5. Number of pokemons in community: 34 out of 258

             #### Community label: 6. Number of pokemons in community: 1 out of 258  

             #### Community label: 7. Number of pokemons in community: 1 out of 258  

             #### Community label: 8. Number of pokemons in community: 1 out of 258  

             #### Community label: 9. Number of pokemons in community: 1 out of 258        
             '''
    elif generation == 3:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
             ## Community info:
             #### Number of communities: 9
             #### Modularity of the network: 0.15516
             #### Community label: 0. Number of pokemons in community: 87 out of 373

             #### Community label: 1. Number of pokemons in community: 62 out of 373

             #### Community label: 2. Number of pokemons in community: 114 out of 373

             #### Community label: 3. Number of pokemons in community: 43 out of 373

             #### Community label: 4. Number of pokemons in community: 63 out of 373

             #### Community label: 5. Number of pokemons in community: 1 out of 373

             #### Community label: 6. Number of pokemons in community: 1 out of 373  

             #### Community label: 7. Number of pokemons in community: 1 out of 373  

             #### Community label: 8. Number of pokemons in community: 1 out of 373     
             '''
    elif generation == 4:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
             ## Community info:
             #### Number of communities: 10
             #### Modularity of the network: 0.16168
             #### Community label: 0. Number of pokemons in community: 99 out of 443

             #### Community label: 1. Number of pokemons in community: 88 out of 443

             #### Community label: 2. Number of pokemons in community: 73 out of 443

             #### Community label: 3. Number of pokemons in community: 39 out of 443

             #### Community label: 4. Number of pokemons in community: 21 out of 443

             #### Community label: 5. Number of pokemons in community: 49 out of 443

             #### Community label: 6. Number of pokemons in community: 71 out of 443  

             #### Community label: 7. Number of pokemons in community: 1 out of 443 

             #### Community label: 8. Number of pokemons in community: 1 out of 443   

             #### Community label: 9. Number of pokemons in community: 1 out of 443     
             '''
    elif generation == 5:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
             ## Community info:
             #### Number of communities: 14
             #### Modularity of the network: 0.18660
             #### Community label: 0. Number of pokemons in community: 1 out of 331

             #### Community label: 1. Number of pokemons in community: 103 out of 331

             #### Community label: 2. Number of pokemons in community: 62 out of 331

             #### Community label: 3. Number of pokemons in community: 46 out of 331

             #### Community label: 4. Number of pokemons in community: 42 out of 331

             #### Community label: 5. Number of pokemons in community: 47 out of 331

             #### Community label: 6. Number of pokemons in community: 24 out of 331 

             #### Community label: 7. Number of pokemons in community: 1 out of 331 

             #### Community label: 8. Number of pokemons in community: 1 out of 331   

             #### Community label: 9. Number of pokemons in community: 1 out of 331 

             #### Community label: 10. Number of pokemons in community: 1 out of 331 

             #### Community label: 11. Number of pokemons in community: 1 out of 331 

             #### Community label: 12. Number of pokemons in community: 1 out of 331     
             '''
    elif generation == 6:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
             ## Community info:
             #### Number of communities: 10
             #### Modularity of the network: 0.15567
             #### Community label: 0. Number of pokemons in community: 94 out of 454

             #### Community label: 1. Number of pokemons in community: 51 out of 454

             #### Community label: 2. Number of pokemons in community: 50 out of 454

             #### Community label: 3. Number of pokemons in community: 92 out of 454

             #### Community label: 4. Number of pokemons in community: 78 out of 454

             #### Community label: 5. Number of pokemons in community: 85 out of 454

             #### Community label: 6. Number of pokemons in community: 1 out of 454  

             #### Community label: 7. Number of pokemons in community: 1 out of 454 

             #### Community label: 8. Number of pokemons in community: 1 out of 454   

             #### Community label: 9. Number of pokemons in community: 1 out of 454     
             '''
    elif generation == 7:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
             ## Community info:
             #### Number of communities: 5
             #### Modularity of the network: 0.15567
             #### Community label: 0. Number of pokemons in community: 132 out of 434

             #### Community label: 1. Number of pokemons in community: 50 out of 434

             #### Community label: 2. Number of pokemons in community: 101 out of 434

             #### Community label: 3. Number of pokemons in community: 52 out of 434

             #### Community label: 4. Number of pokemons in community: 99 out of 434
             '''


@app.callback(
    [Output('distribution-img', 'src'),
     Output('statistics-info', 'children')],
    [Input('statistics-slider', 'value')]
)
def update_statistics(generation):
    image_filename = f'distributions/degree_dist{generation}.png'  # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    if generation == 1:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:
        #### Number of nodes: 154
        #### Number of edges: 5934
        #### Average degree: 77.0649
        #### The graph is not fully connected. Average degree computed on the GCC: 1.476
        #### Global clustering coefficient: 0.7396
        #### Assortativity coefficient: -0.1691  
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free      
        '''
    elif generation == 2:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:   
        #### Number of nodes: 258
        #### Number of edges: 10059
        #### Average degree: 77.9767
        #### The graph is not fully connected. Average degree computed on the GCC: 1.6845
        #### Global clustering coefficient: 0.7043
        #### Assortativity coefficient: -0.2203
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free
        '''
    elif generation == 3:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:
        #### Number of nodes: 373
        #### Number of edges: 16836
        #### Average degree: 90.2735
        #### The graph is not fully connected. Average degree computed on the GCC: 1.752
        #### Global clustering coefficient: 0.6758
        #### Assortativity coefficient: -0.2077      
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free
        '''
    elif generation == 4:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:
        #### Number of nodes: 443
        #### Number of edges: 17820
        #### Average degree: 80.4515
        #### The graph is not fully connected. Average degree computed on the GCC: 1.8155
        #### Global clustering coefficient: 0.6991
        #### Assortativity coefficient: -0.2239       
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free
        '''
    elif generation == 5:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:
        #### Number of nodes: 331
        #### Number of edges: 11549
        #### Average degree: 69.7825
        #### The graph is not fully connected. Average degree computed on the GCC: 1.7793
        #### Global clustering coefficient: 0.773
        #### Assortativity coefficient: -0.2189  
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free
        '''
    elif generation == 6:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:
        #### Number of nodes: 454
        #### Number of edges: 22054
        #### Average degree: 97.1542
        #### The graph is not fully connected. Average degree computed on the GCC: 1.784
        #### Global clustering coefficient: 0.7668
        #### Assortativity coefficient: -0.2364      
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free
        '''
    elif generation == 7:
        return 'data:image/png;base64,{}'.format(encoded_image.decode()), '''
        # Network statistics:
        #### Number of nodes: 434
        #### Number of edges: 28303
        #### Average degree: 130.4286
        #### The graph is fully connected. Average shortest path: 1.6988
        #### Global clustering coefficient: 0.7986
        #### Assortativity coefficient: -0.234    
        #### Based on the histogram and fitted distribution we see that the network is neither random or scale-free
        '''