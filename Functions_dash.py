import dash 
from dash import Dash,dcc,html,callback,Input,Output,State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
import Figure as fig
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



def get_legend_groups(figure):
    """
    Returns a set containing all the legend groups in string format.
        
    Parameters:
    - figure (ploty figure): The figure the legends are to be extracted from.

    Returns:
    set: Set of strings of legend groups.
    """
    if not figure['data']:# or not 'legendgroup' in figure['data']: 'data' not in figure or
        return

    legend_groups = set()
    for trace in figure['data']:
        if 'legendgroup' in trace:
            legend_groups.add(trace['legendgroup'])

    return legend_groups


def split_fig(figure):
    """
    Returns the figure as first value and a set of its legend groups as second.
    
    Returns:
    - figure: The figure
    - set: Set of strings of legend groups.
    """
    return figure, get_legend_groups(figure)


def relayoutData_transform(relayoutData):
    """
    Extracts the x and y range out from a graph's relayoutData object to be used to filter data used in graphs.

    Parameters:
    - relayoutData (ploty plot attribute): The element indicating the xlim and ylim of a plot extracted by a callback function.

    Returns:
    - x_range: [min, max] both the min and max values of the x axis filtered from relayoutData

    - y_range: [min, max] both the min and max values of the y axis filtered from relayoutData
    """
    if relayoutData is None:
        return None, None

    y_range = None
    x_range = None
        
    if 'autosize' in relayoutData:
        return None, None
        
    if 'xaxis.range[0]' in relayoutData or 'xaxis.range[1]' in relayoutData:
        x_range = [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]

    if 'yaxis.range[0]' in relayoutData or 'yaxis.range[1]' in relayoutData:
        y_range = [relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']]

    if "xaxis.autorange" in relayoutData:
         x_range = None

    if "yaxis.autorange" in relayoutData:
        y_range = None
        
    return x_range, y_range


def unpack_mods(data_obj: tuple):
    """
    Extracts the legend group of all points ploted in the graph an returns them in an array.

    Parameters:
    - data_obj (selectedData): The figure element extracted by a callback function input.

    Returns:
    - Array of strings: Array of strings containing all legends ploted in a graph.
    """
    out = []

    for point in data_obj['points']:
        out.append(point['legendgroup'])
    
    return out

# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback functions -------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_callbacks(app):


# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback des graphiques -------------------------------------------------
# ------------------------------------------------------------------------------------------------------
    @callback(
        Output('graph2', 'figure'),
        Input('speed-dropdown', 'value'),
    )
    def update_speed_animation(speed_animation):
        return fig.fig2(speed_animation)
    
    # ------------ Page 2 Line chart ------------------ 
    @callback(
        Output('graph4', 'figure'),
        [Input('variable-dropdown', 'value'),
         Input('annee-slider','value'),
         Input('graph6', 'clickData')
        ]
    )
    def update_density(selected_var,selected_annee, clickData):
        # Filters data if clickData Exists
        if clickData is not None:

            filtered_data = fig.data[fig.data['age_group'] == clickData['points'][0]["label"]]

            return fig.density(selected_var,selected_annee, filtered_data, " " + str(clickData['points'][0]["label"]).lower())# Set title comp to the filtered value
        
        return fig.density(selected_var,selected_annee)
    
    # --------- Page 2 Bar chart ----------------------
    @callback(
        Output('graph5', 'figure'),
        [Input('variable-dropdown', 'value'),
         Input('annee-slider','value'),
         Input('graph6', 'clickData')
        ]
    )
    def update_bar(selected_var,selected_annee, clickData):
        # Filters data if clickData Exists
        if clickData is not None:

            filtered_data = fig.data[fig.data['age_group'] == clickData['points'][0]["label"]]

            return fig.bar(selected_var, selected_annee, filtered_data, str(clickData['points'][0]["label"]).lower())


        return fig.bar(selected_var, selected_annee)
    
    # --------- Page 2 Pie chart ----------------------
    @callback(
        Output('graph6', 'figure'),
        [Input('modalite-dropdown', 'value'),
         Input('annee-slider','value'),
         #Input('graph6','clickData'), # Used to change the color of selected data
        ]
    )
    def update_pie(selected_modalite,selected_annee):

        #Used clickData to determine the color to be used for the pie chart upon selecting one

        return fig.pie_age_grav(selected_modalite,selected_annee) 


    # ------------- Testing callback ---------------------------------------------
    @callback(
        Output('test-out1', 'children'),
        [
         Input('graph6', 'clickData')
        ]
    )
    def update_bar(clickData):
        if clickData is None:
            return "ClickData is None."
        return clickData['points'][0]['label']
    

    @callback(
        Output('test-out2', 'children'),
        [
         Input('graph6', 'restyleData')
        ]
    )
    def update_bar(clickData):
        if clickData is None:
            return "ClickData is None."
        return clickData['points'][0]['label']


# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback de la carte -------------------------------------------------
# ------------------------------------------------------------------------------------------------------

    @app.callback(
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

        fig_map = px.scatter_mapbox(build_selection(fig.data, an, mois, jour, catr, cbsm, atm),#select_data(data,selection=select), 
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
        
        fig_map.update_traces(hovertemplate="<br>".join(["Date : %{customdata[0]}", 
                                                "Heure : %{customdata[1]}", 
                                                "Type de trajet : %{customdata[2]}", 
                                                "Intersection: %{customdata[3]}", 
                                                "Conditions d'éclairage: %{customdata[4]}",
                                                "Nom commune: %{customdata[5]}"])) # Replace the nan's in data set
        
        fig_map.update_layout(legend_title_text = legend_title_selection[unlist(color)],
                        margin={"r":0,"t":0,"l":0,"b":0}
                        #legend={'traceorder':[1,2,3,5,4]}
                        )

        return fig_map
    
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
                sidebar_style = fig.SIDEBAR_HIDEN
                content_style = fig.CONTENT_STYLE1
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = fig.SIDEBAR_STYLE
                content_style = fig.CONTENT_STYLE
                cur_nclick = "SHOW"
        else:
            sidebar_style = fig.SIDEBAR_HIDEN #fig.SIDEBAR_STYLE
            content_style = fig.CONTENT_STYLE1 #fig.CONTENT_STYLE
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
        
        elif pathname == "/page-user":
            return pag.page_usager
        
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
    

# ------------------------------------------------------------------------------------------------------
# --------------------------------- Get selected data test ----------------------------------
# ------------------------------------------------------------------------------------------------------

    @app.callback(
        Output('selected-data-output', 'children'),
        [Input('ex-graph_test', 'selectedData')]
    )
    def display_selected_data(selected_data):
        if selected_data is None:
            return 'No data selected.'

        selected_points = selected_data['points']
        if not selected_points:
            return 'No points selected.'

        selected_values = [f"X value: {point['x']}, Y value: {point['y']}" for point in selected_points]
        return html.Ul([html.Li(value) for value in selected_values])


# ------------------------------------------------------------------------------------------------------
# --------------------------------- Get selected legend ----------------------------------
# ------------------------------------------------------------------------------------------------------

    @app.callback(
        Output('selected-legend-output', 'children'),
        [Input('ex-graph_test', 'selectedData')]
    )
    def display_selected_legend(selected_data):
        if selected_data is None:
            return 'No legend items selected.'

        selected_legend_indices = []
        for trace in fig.fig_seri_reg['data']:
            if 'selectedpoints' in trace['legend']:
                selected_legend_indices.extend(trace['legend']['selectedpoints'])

        if not selected_legend_indices:
            return 'No legend items selected.'

        return f'Selected legend indices: {selected_legend_indices}'
    
# ----------------------------------------------------------------------------------------------------------
    '''
    @app.callback(
        Output('ex-graph_test2', 'figure'),
        #Output('test-output','children'),
        [Input('ex-graph_test1', 'selectedData')]
    )
    def update_scatter_plot2(selected_data):
        if selected_data is None or 'points' not in selected_data:
            # No points selected, return the original figure
            return fig.fig_seri_reg(fig.data)

        # Extract the selected species from the points in the first scatter plot
        selected_reg = [point['legendgroup'] for point in selected_data['points']]#[point['text'] for point in selected_data['points']]

        # Filter the data for the second scatter plot based on the selected species
        filtered_df = fig.data[fig.data['region_name'].isin(selected_reg)]

        # Create a new figure for the second scatter plot with the filtered data
        filtered_fig_seri_reg = fig.fig_seri_reg(filtered_df)

        return filtered_fig_seri_reg
        '''


    

    # ------------------------------------------------------------------------------------------------------
    # --------------------------------- Graph filtering functions ----------------------------------
    # ------------------------------------------------------------------------------------------------------
    
    #pd.read_json("").query()
    '''
    @callback(inputs=[Input("data-page-usager", "data")],
              output=[Output("graph5", "figure"),
                      Output("graph6", "figure")])
    def filter_data_and_plot_group1(data):
        data = pd.read_json(orient="split")
        
        return fig.bar(selected_var,selected_annee), fig.pie_age_grav(selected_modalite,selected_annee)
    '''
    #  Graph filtering functions are organized with one per connection group


    # ------------------------------------------------------------------------------------------------------
    # --------------------------------- Test graphs ----------------------------------
    # ------------------------------------------------------------------------------------------------------

    
    # Selecting 
    @callback(
        Output('ex-graph_test2', 'figure'),
        #Output('test-output','children'),
        Input('ex-graph_test1', 'selectedData'),
        Input('ex-graph_test1', 'relayoutData'),
        Input('ex-graph_test1', 'clickData'))
    def update_x_timeseries(selectedData, relayoutData, clickData):
        # Vecteur containing the the maximum and minimum values ploted on each axis
        x_range = relayoutData_transform(relayoutData)[0]
        y_range = relayoutData_transform(relayoutData)[1]

        if selectedData is None or len(selectedData['points']) == 0:
            return fig.fig_seri_reg(fig.data, x_range, y_range)
        
        dff = fig.data.copy(deep=True)

        # Filter data based on the first region in selection region selected
        reg_name = selectedData['points'][0]['customdata'][1]
        #reg_name = unpack_mods(selectedData)
        dff = dff[dff['region_name'] == reg_name] # replece == with in

        # Filter data based on cliked data
        #if clickData is None or len(clickData['points']) == 0:
        #    dff = dff[dff['col'] == clickData['points'][0]['customdata'][0] and get row]
        """
        if clickData != None or len(clickData['points']) != 0:
            clicked_legend_item = clickData['points'][0]['label']
            filtered_df = dff[dff['species'] == clicked_legend_item]
        """
        return fig.fig_seri_reg(dff, x_range, y_range)