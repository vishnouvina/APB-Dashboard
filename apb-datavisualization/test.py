import numpy as np
import pandas as pd


def dash_carte_critere(df, filiere, critere="fille"):

    def filiere_filiere_fine_ou_sous_filiere(filiere):
        """
        filiere_filiere_fine_ou_sous_filiere permet de renvoyer si l'entrée appartient à la catégorie des filières,
        filières fines ou sous-filières,

        Parameters
        ----------
        filiere : str
            Nom de la filière, filière fine ou filière dont on veut déterminer la catégorie

        Returns
        _______
        "filiere" si l'entrée est une filière
        "filiere_fine" si l'entrée est une filière fine
        "sous_filiere" si l'entrée est une sous_filière
        "non" si aucun des cas ci-dessus
        """

        # On récupère la liste des filières
        liste_des_filieres = liste_filieres(df)

        liste_des_filiere_fine = []
        liste_des_sous_filiere = []
        # On récupère toutes les sous-filières et les filières fines à l'aide des fonctions de data_statistics
        # Pas besoin de retirer les doublons
        for fili in liste_des_filieres:
            liste_des_filiere_fine = liste_des_filiere_fine + \
                liste_filieres_fines(df, fili)
            liste_des_sous_filiere = liste_des_sous_filiere + \
                liste_sous_filiere(df, fili)

        if filiere in liste_des_filieres:
            return 'filiere'
        elif filiere in liste_des_filiere_fine:
            return 'filiere_fine'
        elif filiere in liste_des_sous_filiere:
            return 'sous_filiere'
        else:
            return 'non'

    df_2 = df
    if filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere':
        df_2 = df[df['fili'] == filiere]
        filiere = filiere[2::]
    elif filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere_fine':
        df_2 = df[df['filiere_fine'] == filiere]
    elif filiere_filiere_fine_ou_sous_filiere(filiere) == 'sous_filiere':
        df_2 = df[df['sous_filiere'] == filiere]

    liste_dep = ['Dordogne', 'Doubs', 'Drôme', 'Eure', 'Eure-et-Loir', 'Finistère', 'Gard', 'Haute-Garonne', 'Gironde', 'Hérault', 'Ille-et-Vilaine', 'Indre', 'Indre-et-Loire', 'Isère', 'Jura', 'Landes', 'Loir-et-Cher', 'Loire', 'Haute-Loire', 'Aveyron', 'Bouches-du-Rhône', 'Calvados', 'Cantal', 'Charente', 'Charente-Maritime', 'Ain', 'Aisne', 'Allier', 'Alpes-Maritimes', 'Ardèche', 'Aube', 'Aude', 'Corrèze', "Côte-d'Or", "Côtes-d'Armor", 'Creuse', 'Loire-Atlantique', 'Loiret', 'Lot', 'Maine-et-Loire', 'Tarn', 'Var', 'Vaucluse', 'Vendée', 'Vienne', 'Haute-Vienne', 'Vosges', 'Yonne', 'Morbihan', 'Moselle', 'Nièvre', 'Nord', 'Rhône', 'Haute-Saône', 'Saône-et-Loire',
                 'Sarthe', 'Savoie', 'Haute-Savoie', 'Seine-Maritime', 'Seine-et-Marne', 'Yvelines', 'Deux-Sèvres', 'Somme', 'Pyrénées-Atlantiques', 'Bas-Rhin', 'Haut-Rhin', 'Oise', 'Orne', 'Pas-de-Calais', 'Puy-de-Dôme', 'Val-de-Marne', "Val-d'Oise", 'Corse-du-Sud', 'Haute-Corse', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte', 'Essonne', 'Hauts-de-Seine', 'Seine-Saint-Denis', 'Manche', 'Marne', 'Haute-Marne', 'Mayenne', 'Meurthe-et-Moselle', 'Paris', 'Meuse', 'Lot-et-Garonne', 'Lozère', 'Pyrénées-Orientales', 'Hautes-Pyrénées', 'Cher', 'Alpes-de-Haute-Provence', 'Ardennes', 'Territoire de Belfort', 'Hautes-Alpes', 'Tarn-et-Garonne', 'Ariège', 'Gers']
    print(len(liste_dep))
    liste_pourcentage = []
    for departement in liste_dep:
        if not pd.isnull(departement):
            somme = 0
            somme_tot = 0
            df_3 = df_2[df_2['nom_dep'] == departement]
            liste_nb = []
            if critere == "fille":
                liste_nb = list(df_3['nb_admis_f'])
            elif critere == "boursier":
                liste_nb = list(df_3['nb_boursiers'])
            liste_nb_tot = list(df_3['nb_admis'])
            for i in range(len(liste_nb_tot)):
                somme += int(liste_nb[i])
                somme_tot += int(liste_nb_tot[i])
            if somme_tot != 0:
                liste_pourcentage.append(somme/somme_tot)
            else:
                liste_pourcentage.append(0)
    print(len(liste_dep), len(liste_pourcentage))
    with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
        departements = json.load(response)

    dico_transi = {'nom': liste_dep,
                   'pourcentage': liste_pourcentage}
    df3 = pd.DataFrame(dico_transi)

    fig = px.choropleth_mapbox(df3, geojson=departements, locations='nom', color='pourcentage', featureidkey='properties.nom',
                               color_continuous_scale="Viridis",
                               range_color=(0, 0.7),
                               mapbox_style="carto-positron",
                               zoom=5, center={"lat": 46.5132, "lon": 0},
                               opacity=0.5,
                               labels={
                                   'pourcentage': 'Part de ' + critere},
                               title="Part de " + critere +
                               " dans les études supérieures pour la filière : " + filiere
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


"""
l_finale = moy_attractivite_dep(df, filiere)
    indice = []
    for i in range(len(l_finale)):
        indice.append(l_finale[i][0])
    valeur_max = max(indice)
    valeur_min = min(indice)
    """
