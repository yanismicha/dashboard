import dash 
from dash import Dash,dcc,html,callback,Input,Output,State
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import Figure as fig

# --------------------------------------------------------------------------------------------------
# --------------------------------------- Page d'accueil ---------------------------------------------
# --------------------------------------------------------------------------------------------------


page_main = html.Div([
                html.Div(
                    children=[
                            fig.nb_total,
                            fig.nb_mort,
                            fig.nb_hospital,
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
                        dbc.Col(
                            [
                                 dcc.Dropdown(
                                        id='speed-dropdown',
                                        options=[
                                            {'label': speed, 'value': speed} 
                                             for speed in ["normal","x1.5","x2","x4","x8"]
                                        ],
                                        value="normal",
                                        style={'width': '40%', "margin-bottom": "10px"}
                                 ),
                                dcc.Graph(id='graph2')
                            ], width=6),
                        dbc.Col(dcc.Graph(id='graph1',figure=fig.fig1()), width=6),
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
                dcc.Graph(id='graph3',figure=fig.fig3()),
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
# --------------------------------------- Page situation usager/accidents ---------------------------------------------
# --------------------------------------------------------------------------------------------------
page_usager = html.Div([
                html.Div(
                    html.H1("Description des accidents et états/situation des usagers mis en cause"),
                    style={
                        "border": "0px solid black",
                        "padding": "10px 20px",
                        "border-radius": "25px",
                        "text-align": "center",
                        "box-shadow": "0 0 0 transparent, 0 0 0 transparent, 6px 4px 25px #d6d6d6",
                        "background": "#ffffff",
                        "margin-bottom": "20px",
                        "font-family": "Montserrat, sans-serif",
                    },
                ),
                html.Div(
                    children = [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        "Choix de variable:",
                                        dcc.Dropdown(
                                            id='variable-dropdown',
                                            options=[
                                                {'label': modalite, 'value': modalite} 
                                                for modalite in ["all","grav","situ","trajet","sexe","dep","region_name"]
                                            ],
                                            value="all",
                                            style={'width': '50%', "margin-top": "5px"}
                                        ),
                                        #dcc.Dropdown(
                                         #   id='annee2-dropdown',
                                          #  options=[
                                           #     {'label': modalite, 'value': modalite} 
                                            #    for modalite in fig.mod_year
                                            #],
                                            #value=fig.mod_year[0],
                                            #style={'width': '50%'}
                                        #),
                                    ],
                                    width=12,  # La largeur totale de la colonne est de 12
                                ),
                            ],
                            style={"margin-bottom": "10px"}
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id='graph4'), width=6),
                                dbc.Col(dcc.Graph(id='graph5'), width=6),
                            ],
                        ),
                        dcc.Slider(
                            2004,
                            fig.data['an'].max(),
                            step=None,
                            id='annee-slider',
                            value=fig.data['an'].min(),
                            marks = {**{2004: 'all'}, **{year: str(year) for year in range(2005, 2022)}}
                        )
                    ],
                    style={
                            "border": "0px solid black",
                            "padding": "10px 20px",
                            "border-radius": "25px",
                            "text-align": "left",
                            "box-shadow": "0 0 0 transparent, 0 0 0 transparent, 6px 4px 25px #d6d6d6",
                            "background": "#ffffff",
                            "margin-bottom": "20px"
                        }
                ),
                 html.Div([
                     "Gravité de la blessure:",
                     dcc.Dropdown(
                        id='modalite-dropdown',
                        options=[{'label': modalite, 'value': modalite} for modalite in ["all"] + fig.data["grav"].unique().tolist()],
                        value=fig.data['grav'].unique()[2],  
                        style={'width': '50%'}
                    ),
                    dcc.Graph(id='graph6'),
                 ],
                    style={
                            "border": "0px solid black",
                            "padding": "10px 20px",
                            "border-radius": "25px",
                            "text-align": "left",
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
                html.H1(["Accidentologie en france"], style=fonte),
                html.Div(className= "float-figainer",children=[

    
                    
                    html.Div(id="selection", className="float-child",
                            children=[
                                      html.Div(children=["Selectionner l'année"], style=fonte),
                                      dcc.Dropdown(id='dropdown_an',
                                                  options=fig.data['an'].unique(),
                                                  value="all",
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      #html.Div(id='var_select_text',style={'color': 'white'}),
                                      
                                      html.Div(children=["Selectionner le mois"], style=fonte),
                                      dcc.Dropdown(id='dropdown_mois',
                                                  options=fig.data['mois'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      
                                      html.Div(children=["Selectionner le jour"], style=fonte),
                                      dcc.Dropdown(id='dropdown_jour',
                                                  options=fig.data['jour'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionner catr"], style=fonte),
                                      dcc.Dropdown(id='dropdown_catr',
                                                  options=fig.data['catr'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionner obsm"], style=fonte),
                                      dcc.Dropdown(id='dropdown_obsm',
                                                  options=fig.data['obsm'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionner atm"], style=fonte),
                                      dcc.Dropdown(id='dropdown_atm',
                                                  options=fig.data['atm'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      


                                      # Color ----------------------------------------------------------------------------------
                                      html.Div(children=["Selectionner la variable à être représentée en couleur"], style=fonte),
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