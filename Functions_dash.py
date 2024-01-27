import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data= pd.read_csv("accidents-velos_clean.csv",low_memory=False)
data = data.drop(data[data['sexe']=='-1'].index)
regions_name= pd.read_csv("departements-region.csv")
data= pd.merge(data, regions_name[['num_dep','region_name']], left_on='dep', right_on='num_dep',how='right')
# on ordonne la variable mois pour avoir une année dans l'ordre
mois_ordre = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
# Conversion de la variable 'mois' en facteur ordonnné
data['mois'] = pd.Categorical(data['mois'], categories=mois_ordre, ordered=True)
data['situ'] = data['situ'].replace(['Non renseigné', 'Aucun','Autres','Sur autre voie spéciale'], 'Autres')

def fig1():
    # on calcul les occurences des accidents par année
    accidents_par_annee = data.groupby('an').size().reset_index(name='Nombre_d_accidents')
    # Créer le lineplot pour la courbe évolutive
    fig = px.line(accidents_par_annee, x="an", y="Nombre_d_accidents",
                markers=True,
                custom_data= ['an','Nombre_d_accidents'])
    # taille de la figure (largeur, hauteur)
    fig.update_layout(width=800, height=500,yaxis=dict(range=[0,7500]))
    #  ajout titre et axes
    fig.update_layout(
                    xaxis_title="Année",
                    yaxis_title="Nombre d'accidents")
    fig.update_layout(margin = {"r":0,"t":30,"l":0,"b":0},
                    title={
            'text': "<b>Évolution du nombre d\'accidents de vélos par année sur le territoire français</b>",
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

def fig2():
    accidents_par_annee_mois = data.groupby(['an','mois']).size().reset_index(name = 'Nombre_d_accidents')
    fig2 = px.line(accidents_par_annee_mois, x="mois", y="Nombre_d_accidents", 
                  markers=True,animation_frame="an"
                 ,custom_data=['an','mois','Nombre_d_accidents'])
    # taille de la figure (largeur, hauteur)
    fig2.update_layout(width=800, height=500)
    #  ajout titre et axes
    fig2.update_layout(title="Évolution du nombre d'accidents de vélos par année",
                      xaxis_title="mois",
                      yaxis_title="Nombre d'accidents"
                     )
    # ralentir la vitese d'animation
    fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    
    # changer l'echelle des ordonnées
    fig2.update_yaxes(range=[0, 1100])
    
    # Titre
    fig2.update_layout(margin = {"r":0,"t":30,"l":0,"b":0},
                     title={
            'text': "<b>Évolution du nombre d\'accidents de vélos par année sur le territoire français</b>",
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


def fig3():
    # on récupère les accidents par année et par mois
    accidents_par_annee_mois= data.groupby(['an','mois']).size().reset_index(name='Nombre_d_accidents')
    # Création d'une variable date en fusionnant les années et les mois
    accidents_par_annee_mois['date'] = accidents_par_annee_mois['an'].astype(str) + '-' + accidents_par_annee_mois['mois'].astype(str)
    
    # Création du graphique
    fig3 = px.line(accidents_par_annee_mois, x='date', y='Nombre_d_accidents',
                  labels={'date': 'Date', 'Nombre_d_accidents': 'Nombre d\'accidents'},
                  height=600,
                 custom_data = ['an','mois','Nombre_d_accidents'])
    
    # Ajout de la courbe lissé pour observer une tendance
    smoothed_data = accidents_par_annee_mois['Nombre_d_accidents'].rolling(window=12).mean() # 12 moyenne mobile pour enlever les saisonnalités annuelles
    fig3.add_trace(go.Scatter(x=accidents_par_annee_mois['date'], y=smoothed_data,
                             mode='lines', name='Tendance lissée sur 12 mois'))
    # Titre
    fig3.update_layout(margin = {"r":0,"t":30,"l":0,"b":0},
                     title={
            'text': "<b>Évolution du nombre d\'accidents de vélos par mois sur le territoire français</b>",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20,'family': 'Arial, sans-serif', 'color': 'black'} 
        })
    
    #  slider pour zoomer sur une période donnée
    fig3.update_xaxes(rangeslider_visible=True)
    
    # Personnalisation du popup
    fig3.update_traces(hovertemplate="<br>".join(["Année : %{customdata[0]}",
                                                 "Mois : %{customdata[1]}",
                                                 "Nombre d'accidents : %{customdata[2]}"
                                                 ]),selector= 0)
    
    # Afficher la figure
    return fig3

# Définissez les intervalles et les labels
bins = [0, 18, 30, 50, float('inf')]
labels = ['Moins de 18 ans', 'Entre 18 et 30 ans', 'Entre 30 et 50 ans', 'Plus de 50 ans']

data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

data.groupby("age_group").size()

def pie_age_grav(modalite,annee):
    if annee=="all":
        age_mort = data[data["grav"]==modalite].groupby(["age_group"]).size().reset_index(name= "nb_accidents")
    else:
        age_mort = data[(data["grav"]==modalite) & (data["an"]==annee)].groupby(["age_group"]).size().reset_index(name= "nb_accidents")
    
    labels = age_mort["age_group"]
    values = age_mort["nb_accidents"]
    if modalite == "all":
        data_grav1 = data[data['grav'] == 'Indemne']
        data_grav2 = data[data['grav'] == 'Blessé léger']
        data_grav3 = data[data['grav'] == 'Blessé hospitalisé']
        data_grav4 = data[data['grav'] == 'Tué']
        if annee=="all":
            loc1 = data_grav1.groupby('age_group').size().reset_index(name="nombre_d'accidents")
            loc2 = data_grav2.groupby('age_group').size().reset_index(name="nombre_d'accidents")
            loc3 = data_grav3.groupby('age_group').size().reset_index(name="nombre_d'accidents")
            loc4 = data_grav4.groupby('age_group').size().reset_index(name="nombre_d'accidents")
        else:
            loc1 = data_grav1[data_grav1["an"]==annee].groupby('age_group').size().reset_index(name="nombre_d'accidents")
            loc2 = data_grav2[data_grav2["an"]==annee].groupby('age_group').size().reset_index(name="nombre_d'accidents")
            loc3 = data_grav3[data_grav3["an"]==annee].groupby('age_group').size().reset_index(name="nombre_d'accidents")
            loc4 = data_grav4[data_grav4["an"]==annee].groupby('age_group').size().reset_index(name="nombre_d'accidents")

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
                         dict(text='Tué', x=0.79, y=0.19, font_size=20, showarrow=False)]
            
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
                          height=600                     
        )
    return fig4

variable_names = {
        "grav": "Gravité de la blessure",
        "situ": "Lieux",
        "trajet": "Trajet de l'usager",
        "sexe": "Genre de l'usager",
        "dep": "Département",
        "region_name": "Région"
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
}

def density(variable,annee):
    if variable == "all":
        if annee == "all":
            df = data.groupby("an").size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "an",y = "nb_accidents", custom_data = ['an','nb_accidents'])
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Année : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))
            fig.update_layout(xaxis_title = "Année")
        else:
            df = data[data["an"]==annee].groupby("mois").size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "mois",y = "nb_accidents",custom_data = ['mois','nb_accidents'])
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Mois : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))
    else:
        if annee == "all":
            df = data.groupby(["an",variable]).size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "an",y = "nb_accidents",color=variable,custom_data = ['an','nb_accidents',variable],
                         color_discrete_sequence=color_discrete_map.get(variable, px.colors.qualitative.Set1),
                          category_orders={variable: category_orders.get(variable)})
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Année : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))
            fig.update_layout(xaxis_title = "Année")
        else:
            df = data[data["an"]==annee].groupby(["mois",variable]).size().reset_index(name="nb_accidents")
            fig = px.area(df,x = "mois",y = "nb_accidents",color=variable,custom_data = ['mois','nb_accidents',variable],
                         color_discrete_sequence=color_discrete_map.get(variable, px.colors.qualitative.Set1),
                          category_orders={variable: category_orders.get(variable)})
            fig.update_traces(hovertemplate="<br>".join([
                                                 "Mois : %{customdata[0]}",
                                                 "Nombre d'accidents : %{customdata[1]}"
                                                 ]))

    fig.update_layout(yaxis_title = "Nombre d'accidents",legend_title_text=variable_names.get(variable, variable))
    return fig


def bar(var, annee):
    if var =="all":
        if annee == "all":
            accidents = data.shape[0]
        else: 
            accidents = data[data["an"]==annee].shape[0]
        total_accidents = pd.DataFrame({'Total d\'accidents': [accidents]})
        fig = px.bar(total_accidents, y='Total d\'accidents') 
        fig.update_layout(xaxis_title=annee,yaxis_title = "Nombre d'accidents")
    else:
        if annee == "all":
            accidents_par_var = data.groupby(var).size().reset_index(name="nb_accidents")
        else:
            accidents_par_var = data[data["an"] == annee].groupby(var).size().reset_index(name="nb_accidents")
        accidents_par_var = accidents_par_var.sort_values('nb_accidents', ascending=False)
        fig = px.bar(accidents_par_var, x=var, y="nb_accidents")
        fig.update_layout(xaxis_title=variable_names.get(var, var),yaxis_title = "Nombre d'accidents",legend_title_text=variable_names.get(var, var))
    return fig
