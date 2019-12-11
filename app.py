import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
title_style = {'fontSize': '55px',  'paddingTop': '40px', 'textAlign': 'center'}
header_style = {'fontSize': '40px', 'paddingLeft': '50px', 'paddingTop': '30px'}
para_style = {'fontSize': '20px', 'paddingLeft': '50px', 'paddingRight': '50px', 'paddingTop': '20px'}
para_style_centered = {'fontSize': '20px', 'paddingLeft': '50px', 'paddingRight': '50px', 'paddingTop': '20px',
                       'textAlign': 'center'}
header_style_centered = {'fontSize': '40px', 'paddingLeft': '50px', 'paddingTop': '30px', 'textAlign': 'center'}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True