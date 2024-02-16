#-----------------------------------------Les imports-----------------------------------------#
import dash
import dash_bootstrap_components as dbc
from dash import Dash,dcc,html,callback,Input,Output, Patch, clientside_callback, callback
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template
import pandas as pd 
import plotly.express as px
import Functions_dash as Fun
import Figure as fig
import pages as pag
from PIL import Image
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#-----------------------------------------Notre Application-----------------------------------------#

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME,"src/assets/styles.css"],suppress_callback_exceptions=True
)

# Bar noir en haut de page
navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Menu", outline=True, color="secondary", className="mr-1", id="btn_sidebar"), # Bouton pour le menu
        dbc.Popover(
                    "CLiquez pour ranger/sortir le sidebar",
                    target='btn_sidebar',
                    trigger="hover",
                    placement = "bottom"
                 ), 
        # Select for merge
        dcc.Dropdown(
                    id='zone-data-filter',
                    options=[{"label":"Nationale","value":'all'},
                             {"label":"Régional","value":'reg'},
                             {"label":"Département","value":'dep'}
                            ],
                    value="all",
                    searchable=False,
                    clearable=False,
                    ),
        dbc.Popover([dbc.PopoverHeader("Choix de zone géographique"),
                     dbc.PopoverBody("Vous pouvez choisir la zone géographique à visualiser pour tout le dashboard")
                     ],
                    target='zone-data-filter',
                    trigger="hover",
                    placement = "right",
                    id="popover-zone-geo",
                    ),
        dcc.Dropdown(
                    id='zone-selection',
                    options=[],
                    value=None,
                    searchable=False,
                    clearable=False,
                    placeholder=""
                    )
    ],
    brand="",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
    links_left= True,
)


submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Visualisations"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right me-3"),
                    width="auto",
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Evolution temporelle", href="/page-1/1"),
            dbc.NavLink("Caractéristiques des accidents", href="/page-1/2"),
        ],
        id="submenu-1-collapse",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col("Cartes interactives"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right me-3"),
                    width="auto",
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-2",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("Carte de la France", href="/page-map"),
            dbc.NavLink("Carte par région/départemnt", href="/page-2/2"),
        ],
        id="submenu-2-collapse",
    ),
]


sidebar = html.Div(
    [
        html.H2("DashBike", className="display-4"),
        html.Hr(),
        html.Img(src = Image.open("src/assets/accident_bike.png"),style={"width": "60%",
                                                             "margin-bottom": '10%'}),
        html.P(
            "Vous trouverez ici les différentes pages du dashboard", className="lead"
        ),
        dbc.Nav(submenu_1 + submenu_2, vertical=True,pills=True),
        html.Img(src=Image.open("src/assets/roue.png"),style={"width": "60%",
                                                  "margin-top": '140%'}),
    ],
    #style=fig.SIDEBAR_STYLE,
    className="SIDEBAR_STYLE",
    id="sidebar",
)


content = html.Div(id="page-content", 
                   #style=fig.CONTENT_STYLE,
                   className="CONTENT_STYLE")

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Store(id='data-store', storage_type='session'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)



# Fonction qui appel toute les fonctions callback qui sont dans le fichier Fonction_dash.py
Fun.get_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True,port=8071)