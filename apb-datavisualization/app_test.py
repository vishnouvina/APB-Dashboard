import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from data_analysis import *
from data_analysis_dash import *
from data_statistics import *
from data_utils import *

from dash.dependencies import Output, Input

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# l'appli est sur http://127.0.0.1:8050/

# Liste des labels utilisés pour le menu déroulant (dcc.Dropdown)
liste_labels = ["Nombre de candidatures, de propositions et d'affectations dans les différentes filières",
                "Carte de France colorée selon l'attractivité du département pour une filière donnée",
                "Carte de France des filières accueillant le plus d'élèves par département",
                "Répartition du nombre de voeux de rang 1 selon les filières",
                "Evolution entre 2016 et 2017 de la répartition du nombre de voeux de rang 1 selon les filières",
                "Nombre de places disponibles dans les différentes filières",
                "Nombre d'établissements proposant chaque filière",
                "Proportion de filles dans les différentes filières",
                "Evolution entre 2016 et 2017 de la proportion de filles dans les différentes filières",
                "Proportion de boursiers dans les différentes filières",
                "Evolution entre 2016 et 2017 de la proportion de boursiers dans les différentes filières",
                # Mais cette fonction nécessite (df, etablissement, filiere)
                "Répartition des mentions des élèves admis pour une filière donnée et un établissement donné",
                "Etablissements les plus attractifs au sein d'une filière",
                "Filières les plus attractives au sein d'un même établissement",
                "Proportion d'étudiants allant dans une filière mais dans un voeu n'était pas leur premier choix",
                "Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée"]

# Chargement du dataframe au préalable
df2016_base = load_dataframe(2016)
df2017_base = load_dataframe(2017)

listes_filieres = liste_filieres(df2016_base)
dico_liste_fili = [{'label': listes_filieres[i][2::],
                    'value': listes_filieres[i]} for i in range(len(listes_filieres))]


listes_filiere_fine = liste_filieres_fines(df2016_base, '4_CPGE')
dico_liste_fili_fine = [
    {'label': 'Toutes les filières fines', 'value': 'toutes'}]
for i in range(len(listes_filiere_fine)):
    dico_liste_fili_fine.append(
        {'label': listes_filiere_fine[i], 'value': listes_filiere_fine[i]})


options_choix_type_donnees = []
for i in range(len(liste_labels)):
    options_choix_type_donnees.append(
        {'label': liste_labels[i], 'value': liste_labels[i]})


# Liste des régions
liste_regions = ["France entière", "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne", "Centre-Val de Loire", "Corse", "Grand Est", "Guadeloupe", "Guyane", "Hauts-de-France",
                 "Île-de-France", "La Réunion", "Martinique", "Mayotte", "Normandie", "Nouvelle-Aquitaine", "Occitanie", "Pays de la Loire", "Polynésie-Française",
                 "Provence-Alpes-Côte d’Azur"]
options_regions = []
for i in range(len(liste_regions)):
    options_regions.append(
        {'label': liste_regions[i], 'value': liste_regions[i]})


app.layout = html.Div(children=[
    # Ajout du titre
    html.H1(children='Projet DataViz'),


    # Ajout de la liste déroulante pour choisir les données qu'on veut voir
    html.Div(
        dcc.Dropdown(
            id='type_donnees',
            options=options_choix_type_donnees,
            placeholder='Choisissez un type de données à visualiser',
            value="Nombre de candidatures, de propositions et d'affectations dans les différentes filières"
        )
    ),

    # Ajout du graphique qu'on visualise
    html.Div(
        dcc.Graph(
            id='graphique'
        )
    ),

    html.Br(),

    # Ajout de la liste déroulante pour choisir les données qu'on veut voir
    html.Div(
        dcc.Dropdown(
            id='filiere_carte',
            options=dico_liste_fili,
            placeholder='Choisissez la filière à visualiser',
            value="4_CPGE"
        )
    ),
    # Ajout de la liste déroulante pour choisir les données de la carte
    html.Div(
        dcc.Dropdown(
            id='filiere_fine_carte',
            placeholder='Choisissez la filière fine à visualiser',
            value="toutes"
        )
    ),
    # Ajout de la liste déroulante pour choisir les données qu'on veut voir
    html.Div(
        dcc.Dropdown(
            id='sous_filiere_carte',
            placeholder='Choisissez la sous filière à visualiser'
        )
    ),


    # Ajout du slider
    html.Div([
        dcc.Slider(
            id='slider',
            min=1,
            max=15,
            step=1,
            value=10,
            marks={1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
                   9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15'},
        )], style={'display': 'block', 'width': '50%'}
    ),

    # Ajout de la radio pour savoir si on veut ça sur les filières générales, ou des sous filières
    html.Div(
        dcc.RadioItems(
            id='choix_filiere',
            value='Visualisation sur les filières'
        )
    ),

    html.Br(),

    # Ajout de la Checklist pour savoir les sous-filières qu'on veut considérer
    html.Div(
        dcc.Checklist(
            id='choix_filiere_fine'
        )
    ),

    html.Br(),

    # Ajout d'un textarea pour la liste des établissements
    html.Div(
        dcc.Textarea(
            id='choix_etablissement',
            value='Lycée Louis Le Grand',
            style={'width': '40%'}
        )
    ),

    html.Br(),
])


# Callback pour l'update du graphe
@ app.callback(
    Output('graphique', 'figure'),
    [Input('type_donnees', 'value'),
        Input('choix_filiere', 'value'),
        Input('choix_filiere_fine', 'value'),
        Input('choix_etablissement', 'value'),
        Input('slider', 'value'),
        Input('filiere_carte', 'value'),
        Input('filiere_fine_carte', 'value'),
        Input('sous_filiere_carte', 'value')
     ])
def update_graph(type_donnees, choix_filiere, choix_filiere_fine, choix_etablissement, slider, filiere_carte, filiere_fine_carte, sous_filiere_carte):
    df = df2016_base

    if type_donnees == "Proportion de filles dans les différentes filières":
        # Si on veut les données sur toutes les filières
        if (choix_filiere == 'Visualisation sur les filières'):
            fig = dash_histogramme_taux_critere_par_filiere(
                df, critere='fille')
        else:
            if choix_filiere == 'Visualisation sur les sous-filières':  # Si on veut visualiser sur les filières fines
                fig = dash_histogramme_taux_critere_par_filiere_fine(
                    df, choix_filiere_fine, critere='fille')
            else:  # Si on veut visualiser sur les sous filières
                fig = dash_histogramme_taux_critere_par_sous_filiere(
                    df, choix_filiere_fine, critere='fille')

            # NB : dans le cas où l'utilisateur n'a pas coché de sous filières, mais a quand même demandé la visualisation par sous filières, il y a une erreur, et je sais pas comment régler ça pour l'instant

    elif type_donnees == "Evolution entre 2016 et 2017 de la proportion de filles dans les différentes filières":
        df2017 = df2017_base
        # Si on veut les données sur toutes les filières
        if (choix_filiere == 'Visualisation sur les filières'):
            fig = dash_evolution_histogramme_taux_critere_par_filiere(
                df, df2017, 'fille')
        else:
            if choix_filiere == 'Visualisation sur les sous-filières':  # Si on veut visualiser sur les filières fines
                fig = dash_evolution_histogramme_taux_critere_par_filiere_fine(
                    df, df2017, choix_filiere_fine, 'fille')
            else:  # Si on veut visualiser sur les sous filières
                fig = dash_evolution_histogramme_taux_critere_par_sous_filiere(
                    df, df2017, choix_filiere_fine, 'fille')

    elif type_donnees == "Proportion de boursiers dans les différentes filières":
        # Si on veut les données sur toutes les filières
        if (choix_filiere == 'Visualisation sur les filières'):
            fig = dash_histogramme_taux_critere_par_filiere(
                df, critere='boursier')
        else:
            if choix_filiere == 'Visualisation sur les sous-filières':  # Si on veut visualiser sur les filières fines
                fig = dash_histogramme_taux_critere_par_filiere_fine(
                    df, choix_filiere_fine, critere='boursier')
            else:  # Si on veut visualiser sur les sous filières
                fig = dash_histogramme_taux_critere_par_sous_filiere(
                    df, choix_filiere_fine, critere='boursier')

    elif type_donnees == "Evolution entre 2016 et 2017 de la proportion de boursiers dans les différentes filières":
        df2017 = df2017_base
        # Si on veut les données sur toutes les filières
        if (choix_filiere == 'Visualisation sur les filières'):
            fig = dash_evolution_histogramme_taux_critere_par_filiere(
                df, df2017, 'boursier')
        else:
            if choix_filiere == 'Visualisation sur les sous-filières':  # Si on veut visualiser sur les filières fines
                fig = dash_evolution_histogramme_taux_critere_par_filiere_fine(
                    df, df2017, choix_filiere_fine, 'boursier')
            else:  # Si on veut visualiser sur les sous filières
                fig = dash_evolution_histogramme_taux_critere_par_sous_filiere(
                    df, df2017, choix_filiere_fine, 'boursier')

    elif type_donnees == "Nombre de candidatures, de propositions et d'affectations dans les différentes filières":
        # Si on veut les données sur toutes les filières
        if (choix_filiere == 'Visualisation sur les filières'):
            fig = dash_histogramme_refus_filiere(df)
        else:
            if choix_filiere == 'Visualisation sur les sous-filières':  # Si on veut visualiser sur les filières fines
                fig = dash_histogramme_refus_filere_fine(
                    df, choix_filiere_fine)
            else:  # Si on veut visualiser sur les sous filières
                fig = dash_histogramme_refus_sous_filiere(
                    df, choix_filiere_fine)

    elif type_donnees == "Répartition du nombre de voeux de rang 1 selon les filières":
        fig = dash_histo_plus_demande(df)

    elif type_donnees == "Evolution entre 2016 et 2017 de la répartition du nombre de voeux de rang 1 selon les filières":
        df2017 = df2017_base
        fig = dash_histo_plus_demande_annees(df, df2017)

    elif type_donnees == "Nombre de places disponibles dans les différentes filières":
        fig = dash_camembert_filieres_places_disponibles(df)

    elif type_donnees == "Nombre d'établissements proposant chaque filière":
        fig = dash_camembert_proportion_etablissement_filieres(df)

    elif type_donnees == "Répartition des mentions des élèves admis pour une filière donnée et un établissement donné":
        fig = dash_camembert_mention_par_etablissement_par_filiere2(
            df, choix_etablissement, choix_filiere)

    elif type_donnees == "Etablissements les plus attractifs au sein d'une filière":
        fig = dash_viz_attractivite(choix_filiere, df, slider)

    elif type_donnees == "Filières les plus attractives au sein d'un même établissement":
        fig = dash_attractivite_etablissement(
            choix_etablissement, df, slider, "sous_filiere")

    elif type_donnees == "Proportion d'étudiants allant dans une filière mais dans un voeu n'était pas leur premier choix":
        fig = dash_histogramme_frustration_filieres(df)

    elif type_donnees == "Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée":
        fig = dash_histogramme_excellence_academique(df, choix_filiere, slider)

    elif type_donnees == "Carte de France des filières accueillant le plus d'élèves par département":
        fig = dash_carte_filiere_principale(df)

    elif type_donnees == "Carte de France colorée selon l'attractivité du département pour une filière donnée":
        if filiere_fine_carte != 'toutes':
            if sous_filiere_carte == 'toutes':
                filiere_carte = filiere_fine_carte
            else:
                filiere_carte = sous_filiere_carte

        fig = dash_carte_attractivite(df, filiere_carte)

    return fig


liste_fonctions_necessitant_radio_et_checklist_completes = ["Nombre de candidatures, de propositions et d'affectations dans les différentes filières",
                                                            "Proportion de filles dans les différentes filières",
                                                            "Evolution entre 2016 et 2017 de la proportion de filles dans les différentes filières",
                                                            "Proportion de boursiers dans les différentes filières",
                                                            "Evolution entre 2016 et 2017 de la proportion de boursiers dans les différentes filières"]

liste_fonctions_necessitant_liste_de_tout = ["Etablissements les plus attractifs au sein d'une filière",  # Qui nécessite toutes les filières, toutes les filières fines, etc
                                             "Filières les plus attractives au sein d'un même établissement"]

liste_fonctions_necessitant_liste_filieres = ["Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée",
                                              "Répartition des mentions des élèves admis pour une filière donnée et un établissement donné"]

liste_fonctions_necessitant_liste_etablissements = ["Filières les plus attractives au sein d'un même établissement",
                                                    "Répartition des mentions des élèves admis pour une filière donnée et un établissement donné"]

# Callback pour l'update de la radio (choix de toutes les filières, ou sous filières)


@app.callback(
    Output('choix_filiere', 'options'),
    [Input('type_donnees', 'value')])
def set_choix_filiere_options(type_donnees):
    if type_donnees in liste_fonctions_necessitant_radio_et_checklist_completes:
        return [
            {'label': 'Visualisation sur les filières',
                'value': 'Visualisation sur les filières'},
            {'label': 'Visualisation sur les sous-filières',
                'value': 'Visualisation sur les sous-filières'},  # Filières fines
            {'label': 'Visualisation sur les sous-filières de ces sous-filières',
                'value': 'Visualisation sur les sous-filières de ces sous-filières'}  # Sous filières
        ]

    elif type_donnees in liste_fonctions_necessitant_liste_de_tout:
        if type_donnees == "Etablissements les plus attractifs au sein d'une filière":
            return [
                {'label': 'Licence', 'value': '1_Licence'},
                {'label': 'DUT', 'value': '2_DUT'},
                {'label': 'BTS', 'value': '3_BTS'},
                {'label': 'CPGE', 'value': '4_CPGE'},
                {'label': 'PACES', 'value': '6_PACES'},
                {'label': 'Management', 'value': '7_Management'},
                {'label': 'Ingénieur', 'value': '8_Ingénieur'},
                {'label': 'Autre', 'value': 'Autre'}]
            # Il faudrait aussi lister les sous filières, etc
        else:
            return []

    elif type_donnees in liste_fonctions_necessitant_liste_filieres:
        return [
            {'label': 'Licence', 'value': '1_Licence'},
            {'label': 'DUT', 'value': '2_DUT'},
            {'label': 'BTS', 'value': '3_BTS'},
            {'label': 'CPGE', 'value': '4_CPGE'},
            {'label': 'PACES', 'value': '6_PACES'},
            {'label': 'Management', 'value': '7_Management'},
            {'label': 'Ingénieur', 'value': '8_Ingénieur'},
            {'label': 'Autre', 'value': 'Autre'},
        ]

    else:
        return []

# Callback pour l'update de la checklist


@app.callback(
    Output('choix_filiere_fine', 'options'),
    [Input('type_donnees', 'value')])
def set_choix_filiere_fine_options(type_donnees):
    if type_donnees in liste_fonctions_necessitant_radio_et_checklist_completes:
        return [
            {'label': 'Licence', 'value': '1_Licence'},
            {'label': 'DUT', 'value': '2_DUT'},
            {'label': 'BTS', 'value': '3_BTS'},
            {'label': 'CPGE', 'value': '4_CPGE'},
            {'label': 'PACES', 'value': '6_PACES'},
            {'label': 'Management', 'value': '7_Management'},
            {'label': 'Ingénieur', 'value': '8_Ingénieur'},
            {'label': 'Autre', 'value': 'Autre'},
        ]

    elif type_donnees in liste_fonctions_necessitant_liste_de_tout:
        return []

    elif type_donnees in liste_fonctions_necessitant_liste_filieres:
        return []

    else:
        return []

# Callback pour l'update du choix d'établissement


@app.callback(
    Output('choix_etablissement', 'style'),
    [Input('type_donnees', 'value')])
def set_choix_etablissement_style(type_donnees):
    if type_donnees in liste_fonctions_necessitant_liste_etablissements:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback pour l'update (cacher ou non) le textarea de la carte


@app.callback(
    Output('filiere_carte', 'style'),
    [Input('type_donnees', 'value')])
def set_filiere_carte_style(type_donnees):
    if type_donnees == "Carte de France colorée selon l'attractivité du département pour une filière donnée":
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('filiere_fine_carte', 'style'),
    [Input('type_donnees', 'value')])
def set_filiere_fine_carte_style(type_donnees):
    if type_donnees == "Carte de France colorée selon l'attractivité du département pour une filière donnée":
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('sous_filiere_carte', 'style'),
    [Input('filiere_fine_carte', 'value')])
def set_sous_filiere_carte_style(filiere_fine_carte):
    if filiere_fine_carte != "toutes":
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('filiere_fine_carte', 'options'),
    [Input('filiere_carte', 'value')])
def set_choix_filiere_fine_carte_options(filiere_carte):
    df = df2016_base
    l_fili_fine = liste_filieres_fines(df, filiere_carte)
    l_options = [{'label': 'Toutes les filières fines', 'value': 'toutes'}]
    for i in range(len(l_fili_fine)):
        l_options.append({'label': l_fili_fine[i], 'value': l_fili_fine[i]})
    return l_options


@app.callback(
    Output('sous_filiere_carte', 'options'),
    [Input('filiere_fine_carte', 'value')])
def set_choix_sous_filiere_options(filiere_fine_carte):
    df = df2016_base
    if filiere_fine_carte != 'toutes':
        l_sous_fili = liste_sous_filiere2(df, filiere_fine_carte)
        l_options = [
            {'label': 'Toutes les sous filières de la filière fine', 'value': 'toutes'}]
        for i in range(len(l_sous_fili)):
            l_options.append(
                {'label': l_sous_fili[i], 'value': l_sous_fili[i]})
        return l_options
    else:
        return []


# Callback pour le slider


@app.callback(
    Output('slider', 'style'),
    [Input('type_donnees', 'value')])
def set_slider_style(type_donnees):
    if type_donnees in ["Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée",
                        "Etablissements les plus attractifs au sein d'une filière"]:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Callbacks pour les valeurs par défaut

# Callback pour la radio choix filière
@app.callback(
    Output('choix_filiere', 'value'),
    [Input('type_donnees', 'value')])
def set_choix_filiere_value(type_donnees):
    if type_donnees in liste_fonctions_necessitant_radio_et_checklist_completes:
        return 'Visualisation sur les filières'

    elif type_donnees in liste_fonctions_necessitant_liste_de_tout:
        return '4_CPGE'

    elif type_donnees in liste_fonctions_necessitant_liste_filieres:
        return '4_CPGE'


@app.callback(
    Output('choix_filiere_fine', 'value'),
    [Input('type_donnees', 'value')])
def set_choix_filiere_fine_value(type_donnees):
    if type_donnees in liste_fonctions_necessitant_radio_et_checklist_completes:
        return ['4_CPGE']

    else:
        return []


# Callback pour l'update du choix d'établissement
@app.callback(
    Output('choix_etablissement', 'value'),
    [Input('type_donnees', 'value')])
def set_choix_etablissement_value(type_donnees):
    if type_donnees in liste_fonctions_necessitant_liste_etablissements:
        return 'Lycée Louis Le Grand'


@app.callback(
    Output('filiere_carte', 'value'),
    [Input('type_donnees', 'value')])
def set_filiere_carte_value(type_donnees):
    return '4_CPGE'


@app.callback(
    Output('filiere_fine_carte', 'value'),
    [Input('type_donnees', 'value')])
def set_filiere_fine_carte_value(type_donnees):
    return 'toutes'


@app.callback(
    Output('sous_filiere_carte', 'value'),
    [Input('type_donnees', 'value')])
def set_sous_filiere_carte_value(type_donnees):
    return 'toutes'


if __name__ == '__main__':
    app.run_server(debug=True)
