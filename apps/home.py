import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent as d
from app import title_style, header_style, para_style


layout = html.Div([
    dcc.Markdown('**Pokemon social graph and analysis**', style=title_style),
    dcc.Markdown('**Aim**', style=header_style),
    dcc.Markdown(d("""
        The aim of this project was to create social graphs associated with data fetched from the Bulbapedia website,
        use the graph analysis and NLP techniques learnt during the class and come up with some meaningful, interesting
        analysis of it.
    """), style=para_style),
    dcc.Markdown('**Data source**', style=header_style),
    dcc.Markdown(d("""
        The data was downloaded from Bulbapedia, a WikiMedia fan-made page about Pokemon.
    """), style=para_style),
    dcc.Markdown('**Dataset brief description**', style=header_style),
    dcc.Markdown(d("""
        The dataset consists of:
        * 1097 files of anime episode descriptions (**16.6MB**), including:
            - plot description
            - list of Pokemon and characters occuring in the episode
        * 809 files of Pokemon descriptions (**21.8MB**), including:
            - statistics info
            - biological description
            - description of appearances in manga and anime
            - trivia
    """), style=para_style),
    dcc.Markdown('**Workflow description**', style=header_style),
    dcc.Markdown(d("""
        The following list describes the worflow for this project:
        
        1. Fetch the data from [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page).
        2. Preprocess the data: create list of Pokemon per generation, select information about occuring pokemon per
        each episode, select information about Pokemon occuring in each routes.
        3. Divide work into three parts and create seperate sections:
        - pokemon-episodes graph
        - pokemon-routes graph
        - sentiment analysis of pokemons belonging to the same **Type** category
        More information can be found in the relevant sections.         
        4. Create a website using **Plotly Dash**.
        5. Create an explanatory notebook.
    """), style=para_style),
    dcc.Markdown('**Page navigation**', style=header_style),
    dcc.Markdown(d("""
        To display each section of the report, please select the corresponding title on the navigation bar, on the top
        of the website.
        
        To navigate back to this Home page, please select the navigation bar title (left part).
    """), style=para_style),
    dcc.Markdown('**Graphs traits**', style=header_style),
    dcc.Markdown(d("""
        The generated graphs are **interactive** graphs. It is possible to:
        - display more information about the single/multiple nodes by:
            - hovering over single node
            - clicking on the single node
            - selecting multiple nodes with the lasso/box tools (top right corner of the graph)
        - zoom in and zoom out by:
            - pressing + and - buttons in the graph tools
            - double clicking on the graph (default zoom in, followed by zoom out)
            - selecting an area with a mouse to zoom in
        - move throughout the graph by holding Shift, left mouse button and by hovering the mouse
        
        For more insightful description, visit the [plotly website](https://plot.ly/python/).
    """), style=para_style),
    dcc.Markdown('**Links**', style=header_style),
    dcc.Markdown(d("""
        [Explanatory jupyter notebook](https://nbviewer.jupyter.org/github/rgoodling3/socialgraphsExplainer/blob/master/Explainer%20Notebook.ipynb)
        
        [Github repository](https://github.com/zyngielg/social-graphs-squad) containing notebooks used for data preparation.
        
        [Web app repository](https://github.com/zyngielg/sgi-pokemon) containing the deployed version of the application.
    """), style=para_style),

    dcc.Markdown('**Group members**', style=header_style),
    dcc.Markdown(d("""
        * Riley Goodling
        * Ali Saleem
        * Gustaw Żyngiel
    """), style=para_style)
])

