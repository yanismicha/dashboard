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


page_main = html.Div([
                html.Div(
                    children=[
                            cont.nb_total,
                            cont.nb_mort,
                            cont.nb_hospital,
                    ],
                    style={
                        # My add
                        'text-align': 'center', 
                           'height': '100%', 
                           'display': 'flex', 
                           'flex-direction': 'row', 
                           'justify-content': 'center', 
                           'align-items': 'center',
                        # default style
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
                    dcc.Graph(id='ex-graph',figure=cont.fig_seri_reg),
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
# ----------------------------------------- La carte -----------------------------------------------
# --------------------------------------------------------------------------------------------------

fonte = {'color': 'white', "font-weight": "bold", "margin" : "0 0 1% 0"}

drop_style = {"margin" : "0 0 4% 0"}

page_map = html.Div([
                html.H1(["Accidentologi en france"], style=fonte),
                html.Div(className= "float-container",children=[

    
                    
                    html.Div(id="selection", className="float-child",
                            children=[
                                      html.Div(children=["Selectionné l'année"], style=fonte),
                                      dcc.Dropdown(id='dropdown_an',
                                                  options=cont.data['an'].unique(),
                                                  value="all",
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      #html.Div(id='var_select_text',style={'color': 'white'}),
                                      
                                      html.Div(children=["Selectionné le mois"], style=fonte),
                                      dcc.Dropdown(id='dropdown_mois',
                                                  options=cont.data['mois'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      
                                      html.Div(children=["Selectionné le jour"], style=fonte),
                                      dcc.Dropdown(id='dropdown_jour',
                                                  options=cont.data['jour'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionné catr"], style=fonte),
                                      dcc.Dropdown(id='dropdown_catr',
                                                  options=cont.data['catr'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionné obsm"], style=fonte),
                                      dcc.Dropdown(id='dropdown_obsm',
                                                  options=cont.data['obsm'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionné atm"], style=fonte),
                                      dcc.Dropdown(id='dropdown_atm',
                                                  options=cont.data['atm'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      


                                      # Color ----------------------------------------------------------------------------------
                                      html.Div(children=["Selectionnée la variable a être représenter en couleur"], style=fonte),
                                      dcc.Dropdown(id='dropdown_color',
                                                  options=[{"label":"Gravité de l'accident","value":'grav'},
                                                          {"label":"Aglomération","value":'agg'}, 
                                                          {"label":"Intersection","value":'int'},
                                                          {"label":"Lumière","value":"lum"},
                                                          {"label":"Jour","value":"jour"}], 
                                                  value="grav",
                                                  clearable=False)
                                      #html.Div([" "],id='color_select_text',style={'color': 'white'})
                                      ],
                            style={'width' : '100%'}),
                     
            
                    html.Div(className="float-child",
                             children=[dcc.Graph(id="map"),
                                       html.Div(id="test")],
                             style={'padding' : '0 0 0 2%'}
                            )
                    
            
],style={'display': 'flex', 'flexDirection': 'row'})
])