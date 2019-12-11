# Load the necessary packages
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import json
from scipy.stats import spearmanr
import base64
from app import app, title_style, header_style_centered, header_style, para_style, para_style_centered
from textwrap import dedent as d
from . import styles
import plotly.graph_objects as go

# Precompute all the statistics
poke_df = pd.read_csv('./pokemon_data.csv')
poke_df.Sentiment = poke_df.Sentiment.apply(round, ndigits = 3)

# Get all the found pokemon types
poke_types = poke_df.Type.unique()
corr_dict = {}
corr_dict_stemmed = {}
pokemons_used = {}
for poke_type in poke_types:
    # First get the pokemons with the specific type
    pokemons_by_type = poke_df[poke_df['Type'] == poke_type]

    # Get their sentiment values and their total stats
    pokemons_by_type_sentiment_stemmed = pokemons_by_type['Sentiment_stemmed']
    pokemons_by_type_sentiment = pokemons_by_type['Sentiment']
    pokemons_by_type_total = pokemons_by_type['Total']

    # Check correlation between biology text sentiment and total stats and store it
    corr_coef_stemmed = spearmanr(pokemons_by_type_sentiment_stemmed, pokemons_by_type_total)[0]
    corr_coef = spearmanr(pokemons_by_type_sentiment, pokemons_by_type_total)[0]

    # Only check for correlation if more than 5 pokemons of this type exists
    if len(pokemons_by_type) >= 5:
        pokemons_used[poke_type] = pokemons_by_type
        corr_dict[poke_type] = round(corr_coef, 4)
        corr_dict_stemmed[poke_type] = corr_coef_stemmed

# The types we made wordclouds for
single_types = sorted(poke_df.Type.unique())[119:]

image_filename = 'wordclouds/Bug_wordcloud.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    dcc.Markdown('**Sentiment analysis**', style=title_style),
    html.Div(className='row', children=[
        html.Div(
            dcc.Markdown('**Correlation between sentiment of biology text and total power stats by pokemon type**',
                         style=para_style_centered),
            className='nine columns'
        ),
        html.Div(
            dcc.Markdown('**Pokemons used to compute the statistics for the chosen type**',
                         style=para_style_centered),
            className='three columns'
        ),

    ]),
    html.Div(className='row', children=[
        html.Div(className='nine columns', children=
            dcc.Graph(id='sentiment-power-correlation',
                      figure={
                          'data': [
                              dict(
                                  x=list(corr_dict.keys()),
                                  y=list(corr_dict.values()),
                                  type=  'bar',
                                  textangle = -90
                              ),
                          ],
                          'layout': dict(
                              xaxis={'tickangle': 45},
                              yaxis={'title': 'Spearman correlation', "domain": [-1, 1]},
                              #title= 'Correlation between sentiment of biology text and total power stats by pokemon type',
                              #title_style={'fontSize': '100px'},
                              opacity= 0.7,
                              clickmode= 'event+select'
                          )
                      }),
                 ),

        html.Div(id='Table-for-pokemon',
                 className='three columns',
                style={'fontSize':'15px'},
                 children=[

            html.Table(
                [
                    html.Tr([html.Th(col) for col in ['Pokémon', 'Sentiment', 'Total', 'Generation']])
                ]
                +
                [
                    html.Tr([
                        html.Td(pokemons_used['Bug'].iloc[i][col]) for col in ['Pokémon', 'Sentiment', 'Total', 'Generation']
                    ]) for i in range(min(len(pokemons_used['Bug']), 10))
                ]
            )
        ]),
    ], style={'display': 'block', 'overflow': 'auto', 'paddingLeft': '50px', 'paddingRight': '50px'}),
    dcc.Markdown(d("""
        The correlation statistics was computed for all types of pokémon which had 5 or more pokémons in that 
        respective type. The measure of correlation is between the sentiment value of a pokémons biology paragraph on 
        Bulbapedia and its total power (A sum of 6 of attributes). The Spearman rank correlation was used.
    """), style={'fontSize': '20px', 'paddingLeft': '50px', 'paddingRight': '50px', 'paddingTop': '40px',
                       'textAlign': 'center'}),

    dcc.Markdown('**Wordclouds for different types of pokémon!**', style=header_style_centered),
    html.Div(
        children=[
            html.Img(id='wordcloud-image', src='data:image/png;base64,{}'.format(encoded_image.decode()),
            style=styles['img']),
            dcc.Slider(
                id='wc-slider',
                min=0,
                max=len(single_types)-1,
                value=0,
                marks={count: str(single_type) for count, single_type in enumerate(single_types)}
            )
        ],
        style={'paddingLeft': "50px", 'paddingRight': "50px"}
    )
])


@app.callback(
    Output('wordcloud-image', 'src'),
    [Input('wc-slider', 'value')])
def update_wordcloud(selected_type):
    image_path = f'wordclouds/{single_types[selected_type]}_wordcloud.png'  #
    image_to_encode = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/png;base64,{}'.format(image_to_encode.decode())

@app.callback(
    Output('Table-for-pokemon', 'children'),
    [Input('sentiment-power-correlation', 'clickData')]
)
def update_table(clickData):
    if clickData is None:
        return dcc.Markdown('''### Click on a bar to see the pokemons used to compute the correlation''')
    x = json.loads(json.dumps(clickData))['points'][0]['x']
    if len(pokemons_used[x]) <= 10:
        shown_pokemons = dcc.Markdown(''' ''')
    else:
        shown_pokemons = dcc.Markdown(f'''### Showing 10 out of {len(pokemons_used[x])} pokemons''')
    return [shown_pokemons,
        html.Table(
        [html.Tr([html.Th(col) for col in ['Pokémon', 'Sentiment', 'Total', 'Generation']])] +

        [html.Tr([
            html.Td(pokemons_used[x].iloc[i][col]) for col in ['Pokémon', 'Sentiment', 'Total', 'Generation']
        ]) for i in range(min(len(pokemons_used[x]), 10))]
    )]

