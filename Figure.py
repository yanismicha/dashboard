import dash 
from dash import Dash,dcc,html,callback,Input,Output,State
import dash_bootstrap_components as dbc
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots


# --------------------------------------------------------------------------------------------------
# ------------------------------------------ DATA ------------------------------------------------
# --------------------------------------------------------------------------------------------------
data= pd.read_csv("DataRendu/accidents-velos_clean.csv",low_memory=False)
data = data.drop(data[data['sexe']=='-1'].index)
regions_name= pd.read_csv("DataRendu/departements-region.csv")
data= pd.merge(data, regions_name[['num_dep','region_name']], left_on='dep', right_on='num_dep',how='right')
# on ordonne la variable mois pour avoir une année dans l'ordre
mois_ordre = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
# Conversion de la variable 'mois' en facteur ordonnné
data['mois'] = pd.Categorical(data['mois'], categories=mois_ordre, ordered=True)
jour_ordre = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
data['jour'] = pd.Categorical(data['jour'], categories=jour_ordre, ordered=True)
# on regroupe certaines modalités
data['situ'] = data['situ'].replace(['Non renseigné', 'Aucun','Autres','Sur autre voie spéciale'], 'Autres')
data['obsm'] = data['obsm'].replace([np.nan,'Aucun','Non renseigné'], 'Non renseigné')
data['atm'] = data['atm'].replace([np.nan,'Autre'], 'Autre')

# Définissez les intervalles et les labels
bins = [0, 18, 30, 50, float('inf')]
# ajout d'une variable age catégorielle
labels = ['Moins de 18 ans', 'Entre 18 et 30 ans', 'Entre 30 et 50 ans', 'Plus de 50 ans']
data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)
data.groupby("age_group",observed=False).size()

# on crée un vecteur avec les années triés dans l'ordre
mod = data["an"].unique()
mod.sort()
# on rajoute "all"
mod_year = ["all"] + mod.tolist()




# --------------------------------------------------------------------------------------------------
# ------------------------------------------ Fonctions ------------------------------------------------
# --------------------------------------------------------------------------------------------------
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

    - ans ('all' or [] or vector): Vector containing all the modalities to be used to select an

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

def data_filter(data: pd.DataFrame, x: str = None, y: str = None, x_select: ([] or None)  = None, y_select: ([] or None)  = None):
    """
    Returns the data filtered by maximum and minimun values for both columns x and y in the given dataframe data.
    To be used for filtering graphs based on the zoom of other graphs. 
        
    Parameters:
    - data (pandas data frame): The data to be filtered.

    - x (string): The name of the column in data to be used in plot's x axis.

    - y (string): The name of the column in data to be used in plot's y axis.

    - x_select ([numeric, numeric] or None): The minimum (vector[0]) and maximum (vector[1]) values used to filter the column used for x axis.

    - y_select ([numeric, numeric] or None): The minimum (vector[0]) and maximum (vector[1]) values used to filter the column used for y axis.

    Returns:
    pandas DataFrame: The data filtered by maximum and minimum x and y values.

    Details:
    If x or y are specified but x_select or y_select are not function will return data unfiltered.
    """
    if (x_select != None and x is None) or (y_select != None and y is None):
        raise Exception("If x_select is not None the x can not be None, or if y_select is not None the y can not be None!")

    if (x != None and x not in data.columns.values) or (y != None and y not in data.columns.values):
        raise Exception("x or y are not valid column names!")

    if x_select != None:
        data = data[(data[x] > x_select[0]) & (data[x] < x_select[1])]

    if y_select != None:
        data = data[(data[y] > y_select[0]) & (data[y] < y_select[1])]

    return data





# --------------------------------------------------------------------------------------------------
# ------------------------------------------ Styles ------------------------------------------------
# --------------------------------------------------------------------------------------------------


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "transition": "all 0.5s",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}



CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}





# --------------------------------------------------------------------------------------------------
# --------------------------------------- Les chiffres ---------------------------------------------
# --------------------------------------------------------------------------------------------------

style_div = {'width': '30%', 'display': 'inline-block'}
style_nb_text1 = {'font-size': '100%', 'bottom' : '0%'}#{"margin": "0% 10% 0%"}#{'color' : 'white'}
style_nb = {'font-size': '200%', 'margin' : '0%'}#{"text-align": "center", "margin" : "20px"}#{"display": "flex","justify-content": "center","align-items": "center"}
style_nb_text2 = {'font-size': '100%'}

# Calcule
mort_per = round(data[(data['an'] == data['an'].max()) & (data['grav'] == 'Tué')].count().iloc[0] / data[(data['an'] == data['an'].max()) & (data['grav'] != 'Tué')].count().iloc[0] * 100,
                 0)

hosp_per = round(data[(data['an'] == data['an'].max()) & (data['grav'] == 'Blessé hospitalisé')].count().iloc[0] / data[(data['an'] == data['an'].max()) & (data['grav'] != 'Blessé hospitalisé')].count().iloc[0] * 100,
                 0)

nb_total = html.Div(style=style_div,
                  children=[html.P(style=style_nb_text1,
                                   children=[f"Nombre d'accidents recensés en {data['an'].max()}:"]), 
                            html.B(style=style_nb,
                                   children=[f"{data[(data['an'] == data['an'].max())].count().iloc[0]}"])
                                   ])

nb_mort = html.Div(style=style_div,
                  children=[html.P(style=style_nb_text1,
                                   children=[f"Nombre de morts en {data['an'].max()}:"]), 
                            html.B(style=style_nb,
                                   children=[f"{data[(data['an'] == data['an'].max()) & (data['grav'] == 'Tué')].count().iloc[0]}"]),
                            html.P(style=style_nb_text2,
                                   children=[f"Représente {mort_per}% des accidents totaux."])
                                   ])

nb_hospital = html.Div(style=style_div,
                  children=[html.P(style=style_nb_text1,
                                   children=[f"Nombre d'hospitalisations en {data['an'].max()}:"]), 
                            html.B(style=style_nb,
                                   children=[f"{data[(data['an'] == data['an'].max()) & (data['grav'] == 'Blessé hospitalisé')].count().iloc[0]}"]),
                                   html.P(style=style_nb_text2,
                                   children=[f"Représente {hosp_per}% des accidents totaux."])
                                   ])


# --------------------------------------------------------------------------------------------------
# ------------------------------------------ Graphiques ------------------------------------------------
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
# ----------------------------------------- Serie temp simple -----------------------------------------------
# --------------------------------------------------------------------------------------------------

def fig1():
    # on calcul les occurences des accidents par année
    accidents_par_annee = data.groupby('an').size().reset_index(name='Nombre_d_accidents')
    # Créer le lineplot pour la courbe évolutive
    fig = px.line(accidents_par_annee, x="an", y="Nombre_d_accidents",
                markers=True,
                custom_data= ['an','Nombre_d_accidents'])
    # taille de la figure (largeur, hauteur)
    fig.update_layout(yaxis=dict(range=[0,7500]))#,width=800, height=500)
    #  ajout titre et axes
    fig.update_layout(
                    xaxis_title="Année",
                    yaxis_title="Nombre d'accidents")
    fig.update_layout(margin = {"r":0,"t":30,"l":0,"b":0},
                    title={
            'text': "<b>Évolution des accidents cyclistes sur le territoire français</b>",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20,'family': 'Arial, sans-serif', 'color': 'black'} 
        })

    # Personnalisation du popup
    fig.update_traces(hovertemplate="<br>".join(["Année : %{customdata[0]}",
                                                "Nombre d'accidents : %{customdata[1]}"
                                                ]),selector= 0)

    # Afficher le graphique interactif
    return fig


# --------------------------------------------------------------------------------------------------
# ----------------------------------------- Serie temp animation -----------------------------------------------
# --------------------------------------------------------------------------------------------------


def fig2(speed_animation):
    accidents_par_annee_mois = data.groupby(['an','mois'],observed=False).size().reset_index(name = 'Nombre_d_accidents')
    fig2 = px.line(accidents_par_annee_mois, x="mois", y="Nombre_d_accidents", 
                  markers=True,animation_frame="an"
                 ,custom_data=['an','mois','Nombre_d_accidents'])
    # taille de la figure (largeur, hauteur)
    #fig2.update_layout(width=700, height=500)
    #  ajout titre et axes
    fig2.update_layout(
                      xaxis_title="Mois",
                      yaxis_title="Nombre d'accidents"
                     )
    # la vitese d'animation
    if speed_animation=="x8":
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500/8
    elif speed_animation=="x4":
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500/4
    elif speed_animation=="x2":
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 750
    elif speed_animation=="x1.5":
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    else:
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    
    # changer l'echelle des ordonnées
    fig2.update_yaxes(range=[0, 1100])
    
    # Titre
    fig2.update_layout(margin = {"r":0,"t":30,"l":0,"b":0},
                     title={
            'text': "<b>Accidents cycliste sur une année</b>",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20,'family': 'Arial, sans-serif', 'color': 'black'} 
        })
    
    # Personnalisation du popup
    fig2.update_traces(hovertemplate="<br>".join(["Année : %{customdata[0]}",
                                                 "Mois : %{customdata[1]}",
                                                 "Nombre d'accidents : %{customdata[2]}"
                                                 ]),selector= 0)
    
    return fig2


# --------------------------------------------------------------------------------------------------
# ----------------------------------------- Serie temp avec saisonnalité et tendance -----------------------------------------------
# --------------------------------------------------------------------------------------------------


def fig3():
    # on récupère les accidents par année et par mois
    accidents_par_annee_mois= data.groupby(['an','mois'],observed=False).size().reset_index(name='Nombre_d_accidents')
    # Création d'une variable date en fusionnant les années et les mois
    accidents_par_annee_mois['date'] = accidents_par_annee_mois['an'].astype(str) + '-' + accidents_par_annee_mois['mois'].astype(str)
    # Décomposition de la série
    result = seasonal_decompose(accidents_par_annee_mois['Nombre_d_accidents'], model='additive', period=12)  # période saisonnière de 12 mois
    fig3 = go.Figure()
    # Ajout de la composante observée
    fig3.add_trace(go.Scatter(x=accidents_par_annee_mois['date'], y=result.observed,
                             mode='lines', name='Composante observée',
                             customdata=pd.DataFrame({'an': accidents_par_annee_mois['an'],
                                                     'mois': accidents_par_annee_mois['mois'],
                                                     'Nombre_d_accidents': accidents_par_annee_mois['Nombre_d_accidents']})))
    
    # Ajout de la composante saisonnière
    fig3.add_trace(go.Scatter(x=accidents_par_annee_mois['date'], y=result.seasonal, visible='legendonly',
                             mode='lines', name='Saisonnalité',
                             customdata=pd.DataFrame({'an': accidents_par_annee_mois['an'],
                                                     'mois': accidents_par_annee_mois['mois'],
                                                     'Nombre_d_accidents': accidents_par_annee_mois['Nombre_d_accidents']})))
    
    # Ajout de la composante de tendance
    fig3.add_trace(go.Scatter(x=accidents_par_annee_mois['date'], y=result.trend,
                             mode='lines', name='Tendance',
                             customdata=pd.DataFrame({'an': accidents_par_annee_mois['an'],
                                                     'mois': accidents_par_annee_mois['mois'],
                                                     'Nombre_d_accidents': accidents_par_annee_mois['Nombre_d_accidents']})))
    
    # Ajout de la composante résiduelle
    fig3.add_trace(go.Scatter(x=accidents_par_annee_mois['date'], y=result.resid,  visible='legendonly',
                             mode='lines', name='Résidus',
                             customdata=pd.DataFrame({'an': accidents_par_annee_mois['an'],
                                                     'mois': accidents_par_annee_mois['mois'],
                                                     'Nombre_d_accidents': accidents_par_annee_mois['Nombre_d_accidents']})))
    
    # Titre
    fig3.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0},
                       title={
                           'text': "<b>Évolution temporelle avec lissage sur 12 mois</b>",
                           'y': 0.98,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top',
                           'font': {'size': 20, 'family': 'Arial, sans-serif', 'color': 'black'}
                       })
    
    # Slider pour zoomer sur une période donnée
    fig3.update_xaxes(rangeslider_visible=True)
    
    # Personnalisation du popup
    fig3.update_traces(hovertemplate="<br>".join(["Année : %{customdata[0]}",
                                                  "Mois : %{customdata[1]}",
                                                  "Nombre d'accidents : %{customdata[2]}"
                                                  ]))
    return fig3



# --------------------------------------------------------------------------------------------------
# ----------------------------------------- Pie chart -----------------------------------------------
# --------------------------------------------------------------------------------------------------

def pie_age_grav(modalite,annee):
    if annee==2004:# cas du "all"
        age_mort = data[data["grav"]==modalite].groupby(["age_group"]).size().reset_index(name= "nb_accidents")
    else:
        age_mort = data[(data["grav"]==modalite) & (data["an"]==annee)].groupby(["age_group"],observed=False).size().reset_index(name= "nb_accidents")
    
    labels = age_mort["age_group"]
    values = age_mort["nb_accidents"]
    if modalite == "all":
        data_grav1 = data[data['grav'] == 'Indemne']
        data_grav2 = data[data['grav'] == 'Blessé léger']
        data_grav3 = data[data['grav'] == 'Blessé hospitalisé']
        data_grav4 = data[data['grav'] == 'Tué']
        if annee==2004:# cas du "all"
            loc1 = data_grav1.groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
            loc2 = data_grav2.groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
            loc3 = data_grav3.groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
            loc4 = data_grav4.groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
        else:
            loc1 = data_grav1[data_grav1["an"]==annee].groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
            loc2 = data_grav2[data_grav2["an"]==annee].groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
            loc3 = data_grav3[data_grav3["an"]==annee].groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")
            loc4 = data_grav4[data_grav4["an"]==annee].groupby('age_group',observed=False).size().reset_index(name="nombre_d'accidents")

        values1 = loc1["nombre_d'accidents"].tolist()
        values2 = loc2["nombre_d'accidents"].tolist()
        values3 = loc3["nombre_d'accidents"].tolist()
        values4 = loc4["nombre_d'accidents"].tolist()
        fig4 = make_subplots(rows=2, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}],
                                                    [{'type': 'domain'}, {'type': 'domain'}]])
        
        fig4.add_trace(go.Pie(labels=loc1['age_group'], values=values1, name="Indemne",marker_colors=['#c2f0c2', '#7ccf7c', '#4cae4c', '#238b23'],
                             hovertemplate="Lieu: %{label}<br>Nombre d'accidents: %{value}<br>Pourcentage: %{percent}"),
                      1, 1)
        fig4.add_trace(go.Pie(labels=loc2['age_group'], values=values2, name="Léger",marker_colors=['#add8e6', '#87ceeb', '#6495ed', '#4169e1'],
                             hovertemplate="Lieu: %{label}<br>Nombre d'accidents: %{value}<br>Pourcentage: %{percent}"),
                      1, 2)
        fig4.add_trace(go.Pie(labels=loc3['age_group'], values=values3, name="Blessé hospitalisé",marker_colors=['#ffdab9', '#ffcc80', '#ffa54f', '#ff8c00'],
                             hovertemplate="Lieu: %{label}<br>Nombre d'accidents: %{value}<br>Pourcentage: %{percent}"),
                      2, 1)
        fig4.add_trace(go.Pie(labels=loc4['age_group'], values=values4, name="Tué",marker_colors=['#ffb6c1', '#ff9999', '#ff6666', '#ff3333'],
                             hovertemplate="Lieu: %{label}<br>Nombre d'accidents: %{value}<br>Pourcentage: %{percent}"),
                      2, 2)
        
        
        fig4.update_traces(hole=0.45, hoverinfo="label+percent+name")
        fig4.update_layout(
            height = 800,title= "Proportion d'accidents cycliste par lieux en fonction de la gravité des blessures",
                          title_x=0.5,  # Centré horizontalement
                          title_y=0.98,  # Au-dessus du graphique
                          title_font=dict(size=20),
                         legend=dict(title="Zones:"),
            annotations=[dict(text='Indemne', x=0.2, y=0.81, font_size=20, showarrow=False),
                         dict(text='Léger', x=0.79, y=0.81, font_size=20, showarrow=False),
                         dict(text='Hospitalisé', x=0.195, y=0.19, font_size=20, showarrow=False),
                         dict(text='Tué', x=0.79, y=0.19, font_size=20, showarrow=False)],
                         clickmode="event+select", # This allows for selection of 1 element by cliking on it
                         hovermode="closest" # Recomended if using select in clickmode 
        )
    else:
        if modalite == "Indemne":
            color=['#c2f0c2', '#7ccf7c', '#4cae4c', '#238b23']
        elif modalite == "Blessé léger":
            color = ['#add8e6', '#87ceeb', '#6495ed', '#4169e1']
        elif modalite == "Blessé hospitalisé":
            color = ['#ffdab9', '#ffcc80', '#ffa54f', '#ff8c00']
        else:
            color = ['#ffb6c1', '#ff9999', '#ff6666', '#ff3333']
            
        fig4 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0, 0.2], marker_colors=color)])
        fig4.update_traces(name = modalite,hovertemplate="Age de l'usager: %{label}<br>Nombre d'accidents: %{value}<br>Pourcentage: %{percent}")
        fig4.update_layout(title= "Proportion d'accidents cycliste en fonction de l'âge de l'usager",
                          title_x=0.5,  # Centré horizontalement
                          title_y=0.98,  # Au-dessus du graphique
                          title_font=dict(size=20),
                          legend=dict(title="Age de l'usager:"),
                          height=600,
                          clickmode="event+select", # This allows for selection of 1 element by cliking on it
                          hovermode="closest" # Recomended if using select in clickmode
        )
        # https://plotly.com/python/creating-and-updating-figures/
        #fig4.update_traces(visible=False, selector=dict(attribute = value))
    return fig4


# --------------------------------------------------------------------------------------------------
# ----------------------------------------- Graphiques densités -----------------------------------------------
# --------------------------------------------------------------------------------------------------
variable_names = {
        "grav": "Gravité de la blessure",
        "situ": "Lieux",
        "trajet": "Trajet de l'usager",
        "sexe": "Genre de l'usager",
        "dep": "Département",
        "region_name": "Région",
        "obsm":"Obstacle rencontré",
        "atm":"Météo lors de l'accident",
    }
color_discrete_map = {
        "grav": ['#4cae4c','#6495ed','#ffa54f','#ff6666'],
        "sexe": ['#6495ed','#ff6666']
}
category_orders = {
        "grav": ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"],
        "situ": data["situ"].unique(),
        "trajet": data["trajet"].unique(),
        "sexe": data["sexe"].unique(),
        "dep" : data["dep"].unique(),
        "region_name" : data["region_name"].unique(),
        "catr": ['Route Départementale', 'Voie Communales',
           'Route nationale','Parc de stationnement ouvert à la circulation publique',
           'Autoroute', 'Hors réseau public', 'Routes de métropole urbaine','autre'],
        "obsm": ['Véhicule', 'Piéton','Véhicule sur rail',
       'Animal domestique', 'Animal sauvage','Autre','Non renseigné'],
        "atm":['Normale', 'Temps éblouissant',
       'Temps couvert','Brouillard - fumée','Pluie légère',
       'Pluie forte','Vent fort - tempête','Neige - grêle','Autre']
}


def density(variable, annee, data = data, title_comp=None):
    if variable == "all":
        if annee == 2004: # equivalent a all pour le slider
            df = data.groupby("an",observed=False).size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "an",y = "nb_accidents", custom_data = ['an','nb_accidents'])
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Année : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))
            fig.update_layout(xaxis_title = "Année")
        else:
            df = data[data["an"]==annee].groupby("mois",observed=False).size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "mois",y = "nb_accidents",custom_data = ['mois','nb_accidents'])
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Mois : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))
    else:
        if annee == 2004: # equivalent a all pour le slider
            df = data.groupby(["an",variable],observed=False).size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "an",y = "nb_accidents",color=variable,custom_data = ['an','nb_accidents',variable],
                         color_discrete_sequence=color_discrete_map.get(variable, px.colors.qualitative.Set1),
                          category_orders={variable: category_orders.get(variable)})
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Année : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))
            fig.update_layout(xaxis_title = "Année")
        else:
            df = data[data["an"]==annee].groupby(["mois",variable],observed=False).size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "mois",y = "nb_accidents",color=variable,custom_data = ['mois','nb_accidents',variable],
                         color_discrete_sequence=color_discrete_map.get(variable, px.colors.qualitative.Set1),
                          category_orders={variable: category_orders.get(variable)})
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Mois : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))


    fig.update_layout(yaxis_title = "Nombre d'accidents",legend_title_text=variable_names.get(variable, variable),
                      clickmode="event+select", # This allows for selection of 1 element by cliking on it
                      hovermode="closest")# Recomended if using select in clickmode 

    # Construct title based on input
    if annee==2004:
        title = "Nombres d'accidents par an"
    else:
        title = "Nombres d'accidents par mois"

    if title_comp != None:
        title = title + " pour les " + title_comp

    fig.update_layout(title=title)

    return fig


# --------------------------------------------------------------------------------------------------
# ----------------------------------------- barplot -----------------------------------------------
# --------------------------------------------------------------------------------------------------


def bar(var, annee, data = data, title_comp = None):
    if var =="all":
        if annee == 2004: # equivalent a all pour le slider
            accidents = data.shape[0]
        else: 
            accidents = data[data["an"]==annee].shape[0]
        total_accidents = pd.DataFrame({'Total d\'accidents': [accidents]})
        fig = px.bar(total_accidents, y='Total d\'accidents') 
    else:
        if annee == 2004: # equivalent a all pour le slider
            accidents_par_var = data.groupby(var,observed=False).size().reset_index(name="nb_accidents")
        else:
            accidents_par_var = data[data["an"] == annee].groupby(var).size().reset_index(name="nb_accidents")
        accidents_par_var = accidents_par_var.sort_values('nb_accidents', ascending=False)
        fig = px.bar(accidents_par_var, x=var, y="nb_accidents")
    fig.update_layout(xaxis_title = annee if annee != 2004 else "De 2005 à 2021",yaxis_title = "Nombre d'accidents",legend_title_text=variable_names.get(var, var),
                          clickmode="event+select", # This allows for selection of 1 element by cliking on it
                          hovermode="closest") # Recomended if using select in clickmode
    
    # Construct title based on input
    if annee==2004:
        title = "Nombres d'accidents sur la période 2005-2021"
    else:
        title = "Nombres d'accidents pour l'annee " + str(annee)

    if title_comp != None:
        title = title + " pour les " + title_comp
    

    fig.update_layout(title=title)

    return fig

# --------------------------------------------------------------------------------------------------
# ----------------------------------------- map -----------------------------------------------
# --------------------------------------------------------------------------------------------------
def carte(color, an, mois, jour, catr, cbsm, atm):
        legend_title_selection = {"grav" : "Gravité de l'accident",
                                "int" : "Type d'intersection ou<br>s'est produit l'accident",
                                "lum" : "Conditions d'éclairage<br>du lieu de l'accident",
                                "jour" : "Jour de la semaine"}

        map = px.scatter_mapbox(build_selection(data, an, mois, jour, catr, cbsm, atm),#select_data(data,selection=select), 
                            lat="lat", 
                            lon="long", 
                            mapbox_style="carto-positron", 
                            center={"lat":46.6031, 'lon':1.8883},
                            zoom=4.8,
                            custom_data=["date","hrmn","trajet", "int", "lum", 'nom_commune'],
                            color=unlist(color),
                            #color_discrete_sequence=color_select(unlist(color)),
                            color_discrete_map = {'Blessé léger':'steelblue', 'Blessé hospitalisé':'orange', 'Tué':'red', 'Indemne':'lightgreen'},
                            height=700,
                            width=1000
                            )
        
        map.update_traces(hovertemplate="<br>".join(["Date : %{customdata[0]}", 
                                                "Heure : %{customdata[1]}", 
                                                "Type de trajet : %{customdata[2]}", 
                                                "Intersection: %{customdata[3]}", 
                                                "Conditions d'éclairage: %{customdata[4]}",
                                                "Nom commune: %{customdata[5]}"])) # Replace the nan's in data set
        
        map.update_layout(legend_title_text = legend_title_selection[unlist(color)],
                        margin={"r":0,"t":0,"l":0,"b":0}
                        #legend={'traceorder':[1,2,3,5,4]}
                        )
        return map