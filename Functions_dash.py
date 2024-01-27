import dash 
from dash import Dash,dcc,html,callback,Input,Output,State
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
import content as cont
import pages as pag


def unlist(input):
    """
    Used to unpack dropdown output if it is in a list. Only return first element in list.
     
    Parameters:
    - input (string, numeric, vector): Output from dropdown menu

    Returns:
    string OR numeric: Returns the input outside of the array
    """
    if isinstance(input, list):
        return input[0]
    return input
    
def select_data(data: pd.DataFrame, selection: dict):
    """
    Filters the given data so as to only keep rows containing the specified modalities
        
    Parameters:
    - data (pandas dataframe): The data frame the data is to extracted from

    - selection (dictionary): Dictionnary containing columns and modalities to keep. Only row with the given modalities will be kept.
                              Dict format: {'column_name1' : ['modality1', 'modality2'],
                                            'column_name1' : ['modality1', 'modality2']}

    Returns:
    pandas dataframe: Dataframe containing only rows with the specified modalities
    """
    out = data

    if selection != {} and selection != 'all':
        for i in selection.items():
            out = out[out[i[0]].isin(i[1])]
            
    return out
    
def build_selection(data: pd.DataFrame, 
                    an = 'all',
                    mois = 'all',
                    jour = 'all',
                    catr = 'all',
                    obsm = 'all',
                    atm = 'all'
                    ):
        
    """
    Builds the dictionnary used to select the data in the given data frame using the select_data function.
    Ment to be used with dropdown menus. Each parameter should be given a vector of modalites for that column.
        
    Parameters:
    - data (pandas dataframe): The data frame the data is to extracted from.

    - ans ('all' or [] or vector): Vector containing all the modalities to be used to select ans

    - mois ('all' or [] or vector): Vector containing all the modalities to be used to select mois

    - jour ('all' or [] or vector): Vector containing all the modalities to be used to select jour

    - catr ('all' or [] or vector): Vector containing all the modalities to be used to select catr

    - obsm ('all' or [] or vector): Vector containing all the modalities to be used to select obsm

    - atm ('all' or [] or vector): Vector containing all the modalities to be used to select atm

    Returns:
    pandas dataframe: Dataframe containing only rows with the specified modalities
    """

    out = {}

    if an != 'all' and an != []:
        out['an']=an

    if mois != 'all' and mois != []:
        out['mois']=mois
            
    if jour != 'all' and jour != []:
        out['jour']=jour

    if catr != 'all' and catr != []:
        out['catr']=catr

    if obsm != 'all' and obsm != []:
        out['obsm']=obsm

    if atm != 'all' and atm != []:
        out['atm']=atm

    return select_data(data, out)


def get_callbacks(app):

# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback de la carte -------------------------------------------------
# ------------------------------------------------------------------------------------------------------

    @callback(
        Output('map', 'figure'),
        [Input('dropdown_color', 'value'),
        Input('dropdown_an', 'value'),
        Input('dropdown_mois', 'value'),
        Input('dropdown_jour', 'value'),
        Input('dropdown_catr', 'value'),
        Input('dropdown_obsm', 'value'),
        Input('dropdown_atm', 'value')]
    )
    def update_map(color, an, mois, jour, catr, cbsm, atm):
    
        legend_title_selection = {"grav" : "Gravité de l'accident",
                                "int" : "Type d'intersection ou<br>c'est produit l'accident",
                                "lum" : "Conditions d'éclairage<br>du lieu de l'accident",
                                "jour" : "Jour de la semaine"}

        fig = px.scatter_mapbox(build_selection(cont.data, an, mois, jour, catr, cbsm, atm),#select_data(data,selection=select), 
                            lat="lat", 
                            lon="long", 
                            mapbox_style="carto-positron", 
                            center={"lat":46.18, 'lon':4.7},
                            zoom=3.8,
                            custom_data=["date","hrmn","trajet", "int", "lum", 'nom_commune'],
                            color=unlist(color),
                            #color_discrete_sequence=color_select(unlist(color)),
                            color_discrete_map = {'Blessé léger':'steelblue', 'Blessé hospitalisé':'orange', 'Tué':'red', 'Indemne':'lightgreen'},
                            height=570,
                            width=1000
                            )
        
        fig.update_traces(hovertemplate="<br>".join(["Date : %{customdata[0]}", 
                                                "Heure : %{customdata[1]}", 
                                                "Type de trajet : %{customdata[2]}", 
                                                "Intersection: %{customdata[3]}", 
                                                "Conditions d'éclairage: %{customdata[4]}",
                                                "Nom commune: %{customdata[5]}"])) # Replace the nan's in data set
        
        fig.update_layout(legend_title_text = legend_title_selection[unlist(color)],
                        margin={"r":0,"t":0,"l":0,"b":0}
                        #legend={'traceorder':[1,2,3,5,4]}
                        )

        return fig
    
# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback ????????? -------------------------------------------------
# ------------------------------------------------------------------------------------------------------

    # this function is used to toggle the is_open property of each Collapse
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open





    # this function applies the "open" class to rotate the chevron
    def set_navitem_class(is_open):
        if is_open:
            return "open"
        return ""


    for i in [1, 2]:
        app.callback(
            Output(f"submenu-{i}-collapse", "is_open"),
            [Input(f"submenu-{i}", "n_clicks")],
            [State(f"submenu-{i}-collapse", "is_open")],
        )(toggle_collapse)

        app.callback(
            Output(f"submenu-{i}", "className"),
            [Input(f"submenu-{i}-collapse", "is_open")],
        )(set_navitem_class)


# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback du sidebar -------------------------------------------------
# ------------------------------------------------------------------------------------------------------

    @app.callback(
        [
            Output("sidebar", "style"),
            Output("page-content", "style"),
            Output("side_click", "data"),
        ],

        [Input("btn_sidebar", "n_clicks")],
        [
            State("side_click", "data"),
        ]
    )
    def toggle_sidebar(n, nclick):
        if n:
            if nclick == "SHOW":
                sidebar_style = cont.SIDEBAR_HIDEN
                content_style = cont.CONTENT_STYLE1
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = cont.SIDEBAR_STYLE
                content_style = cont.CONTENT_STYLE
                cur_nclick = "SHOW"
        else:
            sidebar_style = cont.SIDEBAR_STYLE
            content_style = cont.CONTENT_STYLE
            cur_nclick = 'SHOW'

        return sidebar_style, content_style, cur_nclick

# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback selection page principal ----------------------------------
# ------------------------------------------------------------------------------------------------------
        
    @app.callback(Output("page-content", "children"), 
                  [Input("url", "pathname")])
    def render_page_content(pathname):
        # Page d'acceuil
        if pathname in ["/", "/page-main"]:
            return pag.page_main

        # Page avec carte
        elif pathname == "/page-map":
            return pag.page_map
        
        elif pathname == "/page-2/1":
            return html.P("Oh cool, this is page 2.1!")
        
        elif pathname == "/page-2/2":
            return html.P("No way! This is page 2.2!")
        
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )