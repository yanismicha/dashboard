import dash 
from dash import Dash,dcc,html,callback,Input,Output,State
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import content as cont

# --------------------------------------------------------------------------------------------------
# --------------------------------------- Page d'aceuille ---------------------------------------------
# --------------------------------------------------------------------------------------------------


main_page = html.Div([
                html.Div(
                    children=[
                    dbc.Row(
                        [
                            dbc.Col(cont.nb_total, width=3),
                            dbc.Col(cont.nb_mort, width=3),
                            dbc.Col(cont.nb_hospital, width=3),
                            dbc.Col("Info 4", width=3),
                        ],
                    ),
                    ],
                    style={
                        "border": "0px solid black",
                        "padding": "10px 20px",
                        "border-radius": "25px",
                        "text-align": "center",
                        "box-shadow": "0 0 0 transparent, 0 0 0 transparent, 6px 4px 25px #d6d6d6",
                        "background": "#ffffff",
                        "margin-bottom": "20px",
                        "height": "200px"
                    },
                ),
                html.Div(
                    children = [
                        dbc.Row(
                        [
                            dbc.Col( dcc.Graph(id='ex-graph',figure=cont.fig_seri_simple), width=6),
                            dbc.Col( dcc.Graph(id='ex-graph',figure=cont.fig_seri_liss), width=6),
                        ],
                        ),
                    ],
                    style={
                            "border": "0px solid black",
                            "padding": "10px 20px",
                            "border-radius": "25px",
                            "text-align": "center",
                            "box-shadow": "0 0 0 transparent, 0 0 0 transparent, 6px 4px 25px #d6d6d6",
                            "background": "#ffffff",
                            "margin-bottom": "20px"
                        }
                ),
                html.Div(
                    dcc.Graph(id='ex-graph',figure=cont.fig_seri_simple),
                    style={
                            "border": "0px solid black",
                            "padding": "10px 20px",
                            "border-radius": "25px",
                            "text-align": "center",
                            "box-shadow": "0 0 0 transparent, 0 0 0 transparent, 6px 4px 25px #d6d6d6",
                            "background": "#ffffff",
                            "margin-bottom": "20px"
                        }
                ),
                
            ])

# --------------------------------------------------------------------------------------------------
# --------------------------------------- Page avec carte ---------------------------------------------
# --------------------------------------------------------------------------------------------------