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
                html.Div(id = "div-summary",
                    children=[
                            fig.nb_total,
                            fig.nb_mort,
                            fig.nb_hospital,
                    ],
                    style=fig.NUMBER_DIV_STYLE,
                ),
                 dbc.Popover(
                        [
                            dbc.PopoverHeader("Résumé accidentologique"),
                            dbc.PopoverBody([
                        "Quelques chiffres jugés les plus pertinents sur la dernière année collectée. Ces informations sont tirées des données provenant de ",
                        html.A("data.gouv.fr", href="https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2022/", target="_blank"),
                            ]),
                        ],
                        target='div-summary',
                        trigger="hover",
                        placement="top"
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
                                dbc.Popover(
                                        [
                                            dbc.PopoverHeader("Vitesse d'animation"),
                                            dbc.PopoverBody("Vous pouvez choisir la vitesse d'animation parmi 5 possibilités."),
                                        ],
                                        target='speed-dropdown',
                                        trigger="hover",
                                ),
                                dcc.Graph(id='graph2')
                            ], width=6),
                        dbc.Col(dcc.Graph(id='graph1',figure=fig.fig1()), width=6),
                    ],
                     ),
                ],
                style=fig.DIV_STYLE
            ),
             html.Div(
                dcc.Graph(id='graph3',figure=fig.fig3()),
                style=fig.DIV_STYLE,
            ),
            
        ])

# --------------------------------------------------------------------------------------------------
# --------------------------------------- Page situation usager/accidents ---------------------------------------------
# --------------------------------------------------------------------------------------------------
page_usager = html.Div([
                html.Div(
                    html.H1("Description des accidents et état/situation des usagers mis en cause",id = "div-title"),
                    style=fig.DIV_STYLE,
                ),
                dbc.Popover(
                            [
                                dbc.PopoverHeader("Caractéristiques:"),
                                dbc.PopoverBody("Sur cette page, vous retrouverez des graphiques interactifs entre eux permettant d'explorer plus en profondeur les divers facteurs de l'accidentologie en france."),
                            ],
                            target='div-title',
                            trigger="hover",
                            placement="top"
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
                                            options=[{"label":"all","value":'all'},
                                                    {"label":"Gravité de la blessure","value":'grav'},
                                                    {"label":"Lieux","value":'situ'}, 
                                                    {"label":"Trajet","value":'trajet'},
                                                    {"label":"Genre de l'usager","value":"sexe"},
                                                    {"label":"Départements","value":"dep"},
                                                    {"label":"Régions","value":"region_name"},
                                                    {"label":"Type de route","value":"catr"},
                                                    {"label":"Obstacle rencontré","value":"obsm"},
                                                    {"label":"Météo lors de l'accident","value":"atm"},
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
                        ),
                        dbc.Popover(
                            [
                                dbc.PopoverHeader("Slider Année"),
                                dbc.PopoverBody("Vous pouvez choisir une année à visualiser pour  l'ensemble des graphiques de cette page. Si vous souhaitez voir l'ensemble des dernières années, positionnez le slider sur 'all'."),
                            ],
                            target='annee-slider',
                            trigger="hover",
                            placement = "bottom"
                        )
                    ],
                    style=fig.DIV_STYLE
                ),
                 html.Div([
                     "Gravité de la blessure:",
                     dcc.Dropdown(
                        id='modalite-dropdown',
                        options=[{'label': modalite, 'value': modalite} for modalite in ["all"] + fig.data["grav"].unique().tolist()],
                        value=fig.data['grav'].unique()[2],  
                        style={'width': '50%','margin-bottom': '10px'}
                    ),
                    dbc.Button("Reset",id="reset-button",color="secondary", disabled=True),
                    dcc.Graph(id='graph6'),
                 ],
                    style=fig.DIV_STYLE
                 ),
                
            ])



# --------------------------------------------------------------------------------------------------
# ----------------------------------------- La carte -----------------------------------------------
# --------------------------------------------------------------------------------------------------

fonte = {'color': 'black', "font-weight": "bold", "margin" : "0 0 1% 0"}

drop_style = {"margin" : "0 0 4% 0",'width': '70%'}

page_map = html.Div([
                html.H1(["Accidentologie en france"], style=fonte),
                html.Div(className= "float-figainer",children=[

    
                    
                    html.Div(id="selection", className="float-child",
                            children=[
                                      html.Div(children=["Selectionnez l'année:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_an',
                                                  options=fig.mod,
                                                  value="all",
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      #html.Div(id='var_select_text',style={'color': 'white'}),
                                      
                                      html.Div(children=["Selectionnez le mois:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_mois',
                                                  options=fig.data['mois'].cat.categories,
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      
                                      html.Div(children=["Selectionnez le jour:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_jour',
                                                  options=fig.data['jour'].cat.categories,
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionnez le type de route:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_catr',
                                                  options=fig.data['catr'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionnez l'obstacle rencontré lors de l'accident:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_obsm',
                                                  options=fig.data['obsm'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),

                                      html.Div(children=["Selectionnez le temps météorologique:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_atm',
                                                  options=fig.data['atm'].unique(),
                                                  value="all", 
                                                  multi=True, 
                                                  placeholder="all",
                                                  style= drop_style),
                                      


                                      # Color ----------------------------------------------------------------------------------
                                      html.Div(children=["Selectionnez la variable à être représentée en couleur:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_color',
                                                  options=[{"label":"Gravité de l'accident","value":'grav'},
                                                          {"label":"Aglomération","value":'agg'}, 
                                                          {"label":"Intersection","value":'int'},
                                                          {"label":"Lumière","value":"lum"},
                                                          {"label":"Jour","value":"jour"}], 
                                                  value="grav",
                                                  clearable=False,
                                                  style= drop_style)
                                      #html.Div([" "],id='color_select_text',style={'color': 'white'})
                                      ],
                            style={'width' : '100%'}),
                     
            
                    html.Div(className="float-child",
                             children=[dcc.Graph(id="map"),
                                       html.Div(id="test")],
                             style={'padding' : '0 0 0 2%'}
                            )
                    
            
                ],style={'display': 'flex', 'flexDirection': 'row'})
            ],
            style=fig.DIV_STYLE
)
                            

page_map_region_dep = html.Div([
    html.H1(["Accidentologie en france"], style=fonte),
                html.Div(className= "float-figainer",children=[
                    html.Div(id="selection", className="float-child",
                            children=[
                                      html.Div(children=["Sélectionnez le niveau géographique :"], style=fonte),
                                      dcc.Dropdown(id='dropdown_regdep',
                                                   options=[{'label':"Region","value":'reg'},
                                                            {'label':"Département","value":'dep'}],
                                                   value = "reg",
                                                   style=drop_style,
                                      ),
                                      html.Div(children=["Sélectionnez l'indicateur:"], style=fonte),
                                      dcc.Dropdown(id='dropdown_indic',
                                                   options=[{'label':"Nombre d'accidents ","value":'qte'},
                                                            {'label':"Taux pour 1000 habitants","value":'tx'}],
                                                   value = "qte",
                                                   style=drop_style,
                                      ),
                            ],
                            style={'width' : '100%'}),
                    html.Div(className="float-child",
                             children=[dcc.Graph(id="map_region_dep")],
                             style={'padding' : '0 0 0 2%'}
                            )
                ],style={'display': 'flex', 'flexDirection': 'row'})
            ],
            style=fig.DIV_STYLE
)
