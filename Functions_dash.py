import dash 
from dash import Dash,dcc,html,callback,Input,Output,State
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
import Figure as fig
import pages as pag




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
        Output('graph1', 'figure'),
        Input('niv_geo_dropdown', 'value'),
    )
    def update_niv_geo(niv_geo_update):
        return fig.fig1(fig.data,niv_geo_update)


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
         Input('graph6', 'clickData'),
         Input('modalite-dropdown', 'value'),
         Input('graph6', 'figure')
        ]
    )
    def update_density(selected_var,selected_annee, clickData, modalite_dropdown, filter_figure):
        # Filters data if clickData Exists
        if clickData is not None:
            filtered_data = fig.data[fig.data['age_group'] == clickData['points'][0]["label"]]
            # Only fiters this if pie chart is cliked
            if modalite_dropdown != 'all':
                filtered_data = filtered_data[filtered_data['grav'] == modalite_dropdown]
            
            return fig.density(selected_var,selected_annee, filtered_data, " " + str(clickData['points'][0]["label"]).lower())# Set title comp to the filtered value
        
        return fig.density(selected_var,selected_annee)
    
    # --------- Page 2 Bar chart ----------------------
    @callback(
        Output('graph5', 'figure'),
        [Input('variable-dropdown', 'value'),
         Input('annee-slider','value'),
         Input('graph6', 'clickData'),
         Input('modalite-dropdown', 'value')
        ]
    )
    def update_bar(selected_var,selected_annee, clickData, modalite_dropdown):
        # Filters data if clickData Exists
        if clickData is not None:
            filtered_data = fig.data[fig.data['age_group'] == clickData['points'][0]["label"]]
            # Only fiters this if pie chart is cliked
            if modalite_dropdown != 'all':
                filtered_data = filtered_data[filtered_data['grav'] == modalite_dropdown]

            return fig.bar(selected_var, selected_annee, filtered_data, str(clickData['points'][0]["label"]).lower())


        return fig.bar(selected_var, selected_annee)

    # --------- Page 3 pie chart ----------------------
    @callback(
        Output('graph6', 'figure'),
        [Input('modalite-dropdown', 'value'),
         Input('annee-slider','value'),
        ]
    )
    def update_pie(selected_modalite,selected_annee):
        return fig.pie_age_grav(selected_modalite,selected_annee) 


    @app.callback(
        [Output('reset-button', 'disabled'),
         Output('graph6', 'clickData'),
         Output('reset-button', 'n_clicks')],
        [Input('graph6', 'clickData'),
         Input('reset-button', 'n_clicks')]
    )
    def update_button_and_click_data(click_data, n_clicks):
        # Si le bouton a été cliqué, mettez à jour clickData à None et réinitialise le compteur de clics
        if n_clicks is not None:
            new_click_data = None
            reset_button_clicks = None
        else:
            new_click_data = click_data
            reset_button_clicks = 0
    
        # Mettez à jour la propriété 'disabled' du bouton en fonction de la valeur de clickData
        button_disabled = click_data is None
        return button_disabled, new_click_data, reset_button_clicks
# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback des cartes -------------------------------------------------
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
        return fig.carte(color, an, mois, jour, catr, cbsm, atm)

    
    @callback(
            Output('map_region_dep', 'figure'),
            [Input('dropdown_regdep', 'value'),
             Input('dropdown_indic','value')]
    )
    def update_map(zoom_update,indic_update):
        return fig.fig_dep_reg(zoom_update,indic_update)

    
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
            sidebar_style = fig.SIDEBAR_STYLE
            content_style = fig.CONTENT_STYLE
            cur_nclick = 'SHOW'

        return sidebar_style, content_style, cur_nclick

# ------------------------------------------------------------------------------------------------------
# --------------------------------- Callback selection page principal ----------------------------------
# ------------------------------------------------------------------------------------------------------
        
    @app.callback(Output("page-content", "children"), 
                  [Input("url", "pathname")])
    def render_page_content(pathname):
        # Page d'acceuil
        if pathname in ["/", "/page-1/1"]:
            return pag.page_main

        # Page avec carte
        elif pathname == "/page-1/2":
            return pag.page_usager
        
        elif pathname == "/page-map":
            return pag.page_map
        
        elif pathname == "/page-2/2":
            return pag.page_map_region_dep
        
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
    # --------------------------------- Callback region, departement selection -----------------------------
    # ------------------------------------------------------------------------------------------------------

    @app.callback(
    [Output('zone-selection', 'style'),
     Output('zone-selection', 'options'),
     Output('zone-selection', 'placeholder')],
    [Input('zone-data-filter', 'value')]
    )
    def select_geo_zone(value):
        if value != 'all':
            all_options = {
                'all': [],
                'reg': ['84 Auvergne-Rhône-Alpes',
                        '32 Hauts-de-France',
                        '93 Provence-Alpes-Côte d\'Azur',
                        '75 Nouvelle-Aquitaine',
                        '24 Centre-Val de Loire',
                        '27 Bourgogne-Franche-Comté',
                        '28 Normandie',
                        '53 Bretagne',
                        '76 Occitanie',
                        '52 Pays de la Loire',
                        '44 Grand Est',
                        '11 Île-de-France',
                        '94 Corse'
                        ],
                'dep': ['Department 1', 'Department 2', 'Department 3']  # Replace with your department data
            }
    
            if value == "reg":
                text = "e région"
            else:
                text = " département"
    
            return {'display': 'block'}, all_options[value], "Sélectionnez un" + text
    
        return {'display': 'none'}, [], ""