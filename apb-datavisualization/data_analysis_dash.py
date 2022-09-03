# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
import pandas as pd
from data_analysis import *
from data_statistics import *
from data_utils import *
from urllib.request import urlopen
import json


def dash_evolution_histogramme_taux_critere_par_filiere(df2016, df2017, critere='fille'):
    """
    dash_evolution_histogramme_taux_critere_par_filiere renvoie une figure dash montrant l'évolution du taux de personnes répondant à un critère dans les différentes filières entre 2016 et 2017

    Parameters
    ----------
    df2016: le dataframe de 2016 sur lequel on travaille

    df2017: le dataframe de 2017 sur lequel on travaille

    critere: str
        le critère qu'on veut sélectionner, par défaut c'est "être une femme".
        Les choix disponibles sont "boursier" et "fille"

    Returns
    -------
    Une figure dash
    """

    def liste_taux_critere(dataframe, d, critere):
        filieres = list(d.keys())
        n = len(filieres)
        liste_taux_critere = []
        if critere == 'fille':
            recherche = 'nb_admis_f'
        elif critere == 'boursier':
            recherche = 'nb_boursiers'
        else:
            return None
        for i in range(n):
            filiere = d[filieres[i]]
            total_admis = 0
            total_admis_c = 0
            for lycee in filiere:
                total_admis += filiere[lycee]['nb_admis']
                total_admis_c += filiere[lycee][recherche]

            if (total_admis == 0):
                liste_taux_critere.append()

            else:
                liste_taux_critere.append(total_admis_c/total_admis)
        return liste_taux_critere

    d2016 = classification_par_filiere(df2016)
    filieres = list(d2016.keys())
    n = len(filieres)

    d2017 = classification_par_filiere(df2017)
    liste_taux_critere1 = liste_taux_critere(df2016, d2016, critere)
    liste_taux_critere2 = liste_taux_critere(df2017, d2017, critere)

    # Ici, liste_taux_critere1 contient les taux du critere dans les différentes filières pour 2016
    # Et lsite_taux_critere2 pour 2017
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    labels = []
    for i in range(n):
        labels += [filieres[i], filieres[i]]
    couleurs = ["taux en 2016", "taux en 2017"]*n
    valeurs = []

    m = len(liste_taux_critere1)
    for i in range(m):
        valeurs += [liste_taux_critere1[i], liste_taux_critere2[i]]
    df2 = pd.DataFrame({"Filières": labels,
                        "Proportion de " + critere + "s": valeurs,
                        "Catégories": couleurs})

    # Ajout du titre
    title = "Evolution la proportion de "
    if critere == "fille":
        title += "filles"
    elif critere == "boursier":
        title += "boursiers"
    title += " dans les différentes filières"

    fig = px.bar(df2, x="Filières", y="Proportion de " + critere + "s",
                 color="Catégories", barmode="group", title=title)

    return fig


def dash_evolution_histogramme_taux_critere_par_filiere_fine(df2016, df2017, liste_filieres, critere='fille'):
    """
    dash_evolution_histogramme_taux_critere_par_filiere_fine renvoie une figure dash montrant l'évolution du taux de filles dans les différentes filières fines entre 2016 et 2017

    Parameters
    ----------
    df2016: le dataframe de 2016 sur lequel on travaille

    df2017: le dataframe de 2017 sur lequel on travaille

    liste_filieres: list
        liste des filières dont on veut les sous filieres

    critere: str
        Au choix: 'fille' ou 'boursier', en fonction de ce qu'on veut étudier

    Returns
    -------
    Une figure dash
    """

    def liste_taux_critere(dataframe, d, critere):
        filieres = list(d.keys())
        n = len(filieres)
        liste_taux_critere = []
        if critere == 'fille':
            recherche = 'nb_admis_f'
        elif critere == 'boursier':
            recherche = 'nb_boursiers'
        else:
            return "Error : pas le bon critere"
        for i in range(n):
            filiere = d[filieres[i]]
            total_admis = 0
            total_admis_c = 0
            for lycee in filiere:
                total_admis += filiere[lycee]['nb_admis']
                total_admis_c += filiere[lycee][recherche]

            if (total_admis == 0):
                liste_taux_critere.append(0)

            else:
                liste_taux_critere.append(total_admis_c/total_admis)
        return liste_taux_critere

    d2016 = classification_par_filiere_fine(df2016, liste_filieres)
    filieres = list(d2016.keys())
    n = len(filieres)

    d2017 = classification_par_filiere_fine(df2017, liste_filieres)
    liste_taux_critere1 = liste_taux_critere(df2016, d2016, critere)
    liste_taux_critere2 = liste_taux_critere(df2017, d2017, critere)

    # Ici, liste_taux_filles contient les taux de filles dans les différentes filières
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    labels = []
    for i in range(n):
        labels += [filieres[i], filieres[i]]
    couleurs = ["taux en 2016", "taux en 2017"]*n
    valeurs = []

    m = len(liste_taux_critere1)
    for i in range(m):
        valeurs += [liste_taux_critere1[i], liste_taux_critere2[i]]
    df2 = pd.DataFrame({"Filières": labels,
                        "Proportion de " + critere + "s": valeurs,
                        "Catégories": couleurs})

    # Ajout du titre
    title = "Evolution de la proportion de "
    if critere == "fille":
        title += "filles"
    elif critere == "boursier":
        title += "boursiers"
    title += " dans les différentes filières"

    fig = px.bar(df2, x="Filières", y="Proportion de " + critere + "s",
                 color="Catégories", barmode="group", title=title)

    return fig


def dash_evolution_histogramme_taux_critere_par_sous_filiere(df2016, df2017, liste_filieres, critere='fille'):
    """
    dash_evolution_histogramme_taux_critere_par_sous_filiere renvoie un histogramme montrant l'évolution du taux de filles dans les différentes sous filières entre 2016 et 2017

    Parameters
    ----------
    df2016: le dataframe de 2016 sur lequel on travaille

    df2017: le dataframe de 2017 sur lequel on travaille

    liste_filieres: list
        liste des filières dont on veut les sous filieres

    critere: str
        Au choix: 'fille' ou 'boursier', en fonction de ce qu'on veut étudier

    Returns
    -------
    Une figure dash
    """

    def liste_taux_critere(dataframe, d, critere):
        filieres = list(d.keys())
        n = len(filieres)
        liste_taux_critere = []
        if critere == 'fille':
            recherche = 'nb_admis_f'
        elif critere == 'boursier':
            recherche = 'nb_boursiers'
        else:
            return "Error : pas le bon critere"
        for i in range(n):
            filiere = d[filieres[i]]
            total_admis = 0
            total_admis_c = 0
            for lycee in filiere:
                total_admis += filiere[lycee]['nb_admis']
                total_admis_c += filiere[lycee][recherche]

            if (total_admis == 0):
                liste_taux_critere.append(0)

            else:
                liste_taux_critere.append(total_admis_c/total_admis)
        return liste_taux_critere

    d2016 = classification_par_sous_filiere(df2016, liste_filieres)
    filieres = list(d2016.keys())
    n = len(filieres)

    d2017 = classification_par_sous_filiere(df2017, liste_filieres)
    liste_taux_critere1 = liste_taux_critere(df2016, d2016, critere)
    liste_taux_critere2 = liste_taux_critere(df2017, d2017, critere)

    # Ici, liste_taux_filles contient les taux de filles dans les différentes filières
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    labels = []
    for i in range(n):
        labels += [filieres[i], filieres[i]]
    couleurs = ["taux en 2016", "taux en 2017"]*n
    valeurs = []

    m = len(liste_taux_critere1)
    for i in range(m):
        valeurs += [liste_taux_critere1[i], liste_taux_critere2[i]]
    df2 = pd.DataFrame({"Filières": labels,
                        "Proportion de " + critere + "s": valeurs,
                        "Catégories": couleurs})
    # Ajout du titre
    title = "Evolution de la proportion de "
    if critere == "fille":
        title += "filles"
    elif critere == "boursier":
        title += "boursiers"
    title += " dans les différentes filières"

    fig = px.bar(df2, x="Filières", y="Proportion de " + critere + "s",
                 color="Catégories", barmode="group", title=title)

    return fig


def dash_histogramme_taux_critere_par_filiere(df2016, critere='fille'):
    """
    dash_histogramme_taux_critere_par_filiere renvoie une figure dash montrant le taux de personnes répondant à un critère dans les différentes filières

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    critere: str
        le critère qu'on veut sélectionner, par défaut c'est "être une femme".
        Les choix disponibles sont "boursier" et "fille"

    Returns
    -------
    Une figure dash
    """
    def liste_taux_critere(dataframe, d, critere):
        filieres = list(d.keys())
        n = len(filieres)
        liste_taux_critere = []
        if critere == 'fille':
            recherche = 'nb_admis_f'
        elif critere == 'boursier':
            recherche = 'nb_boursiers'
        else:
            return None
        for i in range(n):
            filiere = d[filieres[i]]
            total_admis = 0
            total_admis_c = 0
            for lycee in filiere:
                total_admis += filiere[lycee]['nb_admis']
                total_admis_c += filiere[lycee][recherche]

            if (total_admis == 0):
                liste_taux_critere.append()

            else:
                liste_taux_critere.append(total_admis_c/total_admis)
        return liste_taux_critere

    d2016 = classification_par_filiere(df2016)
    filieres = list(d2016.keys())
    n = len(filieres)

    liste_taux_critere1 = liste_taux_critere(df2016, d2016, critere)

    # Ici, liste_taux_critere1 contient les taux du critere dans les différentes filières pour 2016
    # Et lsite_taux_critere2 pour 2017
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    labels = filieres
    couleurs = ["Taux en 2016"]*n
    valeurs = liste_taux_critere1

    m = len(liste_taux_critere1)
    df2 = pd.DataFrame({"Filières": labels,
                        "Proportion de " + critere + "s": valeurs,
                        "Catégories": couleurs})

    # Ajout du titre
    title = "Proportion de "
    if critere == "fille":
        title += "filles"
    elif critere == "boursier":
        title += "boursiers"
    title += " dans les différentes filières"

    fig = px.bar(df2, x="Filières", y="Proportion de " + critere + "s",
                 color="Catégories", barmode="group", title=title)

    return fig


def dash_histogramme_taux_critere_par_filiere_fine(df2016, liste_filieres, critere='fille'):
    """
    dash_histogramme_taux_critere_par_filiere_fine renvoie une figure dash montrant le taux de filles dans les différentes filières fines

    Parameters
    ----------
    df2016: le dataframe sur lequel on travaille

    liste_filieres: list
        liste des filières dont on veut les sous filieres

    critere: str
        Au choix: 'fille' ou 'boursier', en fonction de ce qu'on veut étudier

    Returns
    -------
    Une figure dash
    """

    def liste_taux_critere(dataframe, d, critere):
        filieres = list(d.keys())
        n = len(filieres)
        liste_taux_critere = []
        if critere == 'fille':
            recherche = 'nb_admis_f'
        elif critere == 'boursier':
            recherche = 'nb_boursiers'
        else:
            return "Error : pas le bon critere"
        for i in range(n):
            filiere = d[filieres[i]]
            total_admis = 0
            total_admis_c = 0
            for lycee in filiere:
                total_admis += filiere[lycee]['nb_admis']
                total_admis_c += filiere[lycee][recherche]

            if (total_admis == 0):
                liste_taux_critere.append(0)

            else:
                liste_taux_critere.append(total_admis_c/total_admis)
        return liste_taux_critere

    d2016 = classification_par_filiere_fine(df2016, liste_filieres)
    filieres = list(d2016.keys())
    n = len(filieres)

    liste_taux_critere1 = liste_taux_critere(df2016, d2016, critere)

    # Ici, liste_taux_filles contient les taux de filles dans les différentes filières
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    labels = filieres
    couleurs = ["Taux"]*n
    valeurs = liste_taux_critere1

    m = len(liste_taux_critere1)
    df2 = pd.DataFrame({"Filières": labels,
                        "Proportion de " + critere + "s": valeurs,
                        "Catégories": couleurs})

    # Ajout du titre
    title = "Proportion de "
    if critere == "fille":
        title += "filles"
    elif critere == "boursier":
        title += "boursiers"
    title += " dans les différentes filières"

    fig = px.bar(df2, x="Filières", y="Proportion de " + critere + "s",
                 color="Catégories", barmode="group", title=title)

    return fig


def dash_histogramme_taux_critere_par_sous_filiere(df2016, liste_filieres, critere='fille'):
    """
    dash_histogramme_taux_critere_par_sous_filiere renvoie une figure dash montrant le taux de filles dans les différentes sous filières

    Parameters
    ----------
    df2016: le dataframe sur lequel on travaille

    liste_filieres: list
        liste des filières dont on veut les sous filieres

    critere: str
        Au choix: 'fille' ou 'boursier', en fonction de ce qu'on veut étudier

    Returns
    -------
    Une figure dash
    """

    def liste_taux_critere(dataframe, d, critere):
        filieres = list(d.keys())
        n = len(filieres)
        liste_taux_critere = []
        if critere == 'fille':
            recherche = 'nb_admis_f'
        elif critere == 'boursier':
            recherche = 'nb_boursiers'
        else:
            return "Error : pas le bon critere"
        for i in range(n):
            filiere = d[filieres[i]]
            total_admis = 0
            total_admis_c = 0
            for lycee in filiere:
                total_admis += filiere[lycee]['nb_admis']
                total_admis_c += filiere[lycee][recherche]

            if (total_admis == 0):
                liste_taux_critere.append(0)

            else:
                liste_taux_critere.append(total_admis_c/total_admis)
        return liste_taux_critere

    d2016 = classification_par_sous_filiere(df2016, liste_filieres)
    filieres = list(d2016.keys())
    n = len(filieres)

    liste_taux_critere1 = liste_taux_critere(df2016, d2016, critere)

    # Ici, liste_taux_filles contient les taux de filles dans les différentes filières
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    labels = filieres
    couleurs = ["Taux"]*n
    valeurs = liste_taux_critere1

    m = len(liste_taux_critere1)
    df2 = pd.DataFrame({"Filières": labels,
                        "Proportion de " + critere + "s": valeurs,
                        "Catégories": couleurs})
    # Ajout du titre
    title = "Proportion de "
    if critere == "fille":
        title += "filles"
    elif critere == "boursier":
        title += "boursiers"
    title += " dans les différentes filières"

    fig = px.bar(df2, x="Filières", y="Proportion de " + critere + "s",
                 color="Catégories", barmode="group", title=title)

    return fig


def dash_histogramme_refus_filiere(df):
    """
    histogramme_refus_filieres_dash renvoie une figure dash représentant pour chaque filière
    la juxtaposition du nb de candidats, de personnes acceptées et de personnes qui ont validé

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    Returns
    -------
    Une figure dash
    """

    res = voeux_propositions_acceptations(df)
    l_filieres = liste_filieres(df)

    # Création de la figure dash :
    n = len(l_filieres)

    capa_filieres = capacite_par_filiere(df)

    l_c = [int(res[i]['nb_candidatures'])/int(capa_filieres[i]['capacite'])
           for i in res.keys()]
    l_p = [int(res[i]['nb_propositions'])/int(capa_filieres[i]['capacite'])
           for i in res.keys()]
    l_a = [int(res[i]['nb_acceptations'])/int(capa_filieres[i]['capacite'])
           for i in res.keys()]

    Labels = []
    Couleurs = ["Nombre de candidatures à cette filière",
                "Nombres de propositions faites aux étudiants",
                "Nombres d'étudiants ayant accepté cette filière"]*n
    Valeurs = []

    for i in range(n):
        Valeurs += [l_c[i], l_p[i], l_a[i]]
        Labels += [l_filieres[i]]*3

    df2 = pd.DataFrame({
        "Filières": Labels,
        "Taux ramenés aux capacités respectives des filières": Valeurs,
        "Catégories": Couleurs
    })

    fig = px.bar(df2, x="Filières", y="Taux ramenés aux capacités respectives des filières", title="Nombre de candidatures, de propositions et d'affectations dans les différentes filières",
                 color="Catégories", barmode="group")
    return fig


def dash_histogramme_refus_filere_fine(df, l_filieres):
    """
    dash_histogramme_refus_sous_filieres renvoie une figure dash représentant pour chaque filiere fine choisie
    la juxtaposition du nb de candidats, de personnes acceptées et de personnes qui ont validé

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    l_filieres: la liste des filieres desquelles on veut extraire les filieres fines
    Returns
    -------
    Une figure dash
    """

    def dico_int(df, l_sous_filieres):
        res = dict()

        for i in l_sous_filieres:
            # on recupere la liste des caractéristiques de cette ss filiere
            l_c = list(df[df['filiere_fine'] == i]["voe_tot"])
            l_c_int = [int(l_c[i]) for i in range(len(l_c))]
            l_p = list(df[df['filiere_fine'] == i]["prop_tot"])
            l_p_int = [int(l_p[i]) for i in range(len(l_p))]
            l_a = list(df[df['filiere_fine'] == i]["nb_admis"])
            l_a_int = [int(l_a[i]) for i in range(len(l_a))]

            # nb_candidats représente le nombre de candidats à une ss-filière, nb_propositions le nombre de
            # candidats qui se sont vus proposer la filière fine et nb_acceptations le nb de candidats qui l'ont accepté
            res[i] = {'nb_candidatures': sum(l_c_int), 'nb_propositions': sum(
                l_p_int), 'nb_acceptations': sum(l_a_int)}

        return res

    l_filieres_fines = []
    for filiere in l_filieres:
        l_filieres_fines += liste_filieres_fines(df, filiere)

    res = dico_int(df, l_filieres_fines)

    # Affichage de l'histogramme :
    n = len(l_filieres_fines)

    capa_filieres_fines = capacite_par_filiere_fine(df, l_filieres)

    l_c = [int(res[i]['nb_candidatures']) /
           int(capa_filieres_fines[i]['capacite']) for i in res.keys()]
    l_p = [int(res[i]['nb_propositions']) /
           int(capa_filieres_fines[i]['capacite']) for i in res.keys()]
    l_a = [int(res[i]['nb_acceptations']) /
           int(capa_filieres_fines[i]['capacite']) for i in res.keys()]

    Labels = []
    Couleurs = ["Nombre de candidatures à cette filière",
                "Nombres de propositions faites aux étudiants",
                "Nombres d'étudiants ayant accepté cette filière"]*n
    Valeurs = []

    for i in range(n):
        Valeurs += [l_c[i], l_p[i], l_a[i]]
        Labels += [l_filieres_fines[i]]*3

    df2 = pd.DataFrame({
        "Filières": Labels,
        "Taux ramenés aux capacités respectives des filières": Valeurs,
        "Catégories": Couleurs
    })

    titre_intermediaire = ""
    for i in range(len(l_filieres)):
        titre_intermediaire += l_filieres[i]
    titre = "Nombre de candidatures, de propositions et d'affectations dans les différentes filières : " + titre_intermediaire

    fig = px.bar(df2, x="Filières", y="Taux ramenés aux capacités respectives des filières",
                 color="Catégories", barmode="group", title=titre)

    return fig


def dash_histogramme_refus_sous_filiere(df, l_filieres):
    """
    dash_histogramme_refus_sous_filieres renvoie une figure dash représentant pour chaque sous filiere choisie
    la juxtaposition du nb de candidats, de personnes acceptées et de personnes qui ont validé

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    l_filieres: la liste des filieres desquelles on veut extraire les sous filieres
    Returns
    -------
    Une figure dash
    """

    def dico_int(df, l_sous_filieres):
        res = dict()

        for i in l_sous_filieres:
            # on recupere la liste des caractéristiques de cette ss filiere
            l_c = list(df[df['sous_filiere'] == i]["voe_tot"])
            l_c_int = [int(l_c[i]) for i in range(len(l_c))]
            l_p = list(df[df['sous_filiere'] == i]["prop_tot"])
            l_p_int = [int(l_p[i]) for i in range(len(l_p))]
            l_a = list(df[df['sous_filiere'] == i]["nb_admis"])
            l_a_int = [int(l_a[i]) for i in range(len(l_a))]

            # nb_candidats représente le nombre de candidats à une ss-filière, nb_propositions le nombre de
            # candidats qui se sont vus proposer la filière fine et nb_acceptations le nb de candidats qui l'ont accepté
            res[i] = {'nb_candidatures': sum(l_c_int), 'nb_propositions': sum(
                l_p_int), 'nb_acceptations': sum(l_a_int)}

        return res

    l_sous_filieres = []
    for filiere in l_filieres:
        l_sous_filieres += liste_sous_filiere(df, filiere)

    res = dico_int(df, l_sous_filieres)

    # Affichage de l'histogramme :
    n = len(l_sous_filieres)

    capa_sous_filieres = capacite_par_sous_filiere(df, l_filieres)

    l_c = [int(res[i]['nb_candidatures']) /
           int(capa_sous_filieres[i]['capacite']) for i in res.keys()]
    l_p = [int(res[i]['nb_propositions']) /
           int(capa_sous_filieres[i]['capacite']) for i in res.keys()]
    l_a = [int(res[i]['nb_acceptations']) /
           int(capa_sous_filieres[i]['capacite']) for i in res.keys()]

    Labels = []
    Couleurs = ["Nombre de candidatures à cette filière",
                "Nombres de propositions faites aux étudiants",
                "Nombres d'étudiants ayant accepté cette filière"]*n
    Valeurs = []

    for i in range(n):
        Valeurs += [l_c[i], l_p[i], l_a[i]]
        Labels += [l_sous_filieres[i]]*3

    df2 = pd.DataFrame({
        "Filières": Labels,
        "Taux ramenés aux capacités respectives des filières": Valeurs,
        "Catégories": Couleurs
    })

    titre_intermediaire = ""
    for i in range(len(l_filieres)):
        titre_intermediaire += l_filieres[i]
    titre = "Nombre de candidatures, de propositions et d'affectations dans les différentes filières : " + titre_intermediaire

    fig = px.bar(df2, x="Filières", y="Taux ramenés aux capacités respectives des filières",
                 color="Catégories", barmode="group", title=titre)

    return fig


def dash_histo_plus_demande(df2016):
    """
    histo_plus_demande renvoie le graphique montrant la répartition des voeux de rang 1 selon les différentes
    filières pour une année donnée.

    Parameters
    ----------
    df2016 : le dataframe sur lequel on travaille

    Returns
    -------
    Histogramme sous forme de figure dash (version dash)

    """
    liste_fil = liste_filieres(df2016)
    dico = classification_par_filiere(df2016)
    Y = []
    S = 0  # la somme de tous les voeux de rang 1
    for filiere in liste_fil:
        c = 0  # le nombre de rang 1 pour une filière
        for keys in dico[filiere]:
            c += dico[filiere][keys]['nb_voeu1']
            S += dico[filiere][keys]['nb_voeu1']
        Y.append(c)
    for i in range(len(Y)):
        Y[i] = Y[i]/S
    df = pd.DataFrame(
        {'Filières': liste_fil, 'Pourcentage de voeux de rang 1': Y})
    titre = "Répartition des voeux de rang 1 selon les différentes filières"
    fig = px.bar(df, x='Filières',
                 y='Pourcentage de voeux de rang 1', title=titre)

    # app.layout = html.Div(children=[
    # html.H1(children='Répartition des premiers voeux selon les filières'),

    # html.Div(children='''
    # Dash: A web application framework for Python.
    # '''),

    # dcc.Graph(
    # id='example-graph',
    # figure=fig
    # )
    # ])
    return fig


def dash_histo_plus_demande_annees(df2016, df2017):
    """
    Renvoie l'évolution de la répartition des voeux de rang1 entre 2016 et 2017

    Parameters
    ----------
    df2016 : dataframe de 2016
    df2017 : dataframe de 2017

    Returns
    -------
    Histogramme sous forme de figure (version dash)
    """
    liste_fil = liste_filieres(df2016)
    dico_2016 = classification_par_filiere(df2016)
    dico_2017 = classification_par_filiere(df2017)
    Y_2016 = []
    Y_2017 = []
    S_2016 = 0
    S_2017 = 0  # la somme de tous les voeux de rang 1
    for filiere in liste_fil:
        c_2016 = 0  # le nombre de rang 1 pour une filière
        for keys in dico_2016[filiere]:
            c_2016 += dico_2016[filiere][keys]['nb_voeu1']
            S_2016 += dico_2016[filiere][keys]['nb_voeu1']
        Y_2016.append(c_2016)

    for i in range(len(Y_2016)):
        Y_2016[i] = Y_2016[i]/S_2016

    for filiere in liste_fil:
        c_2017 = 0  # le nombre de rang 1 pour une filière
        for keys in dico_2017[filiere]:
            c_2017 += dico_2017[filiere][keys]['nb_voeu1']
            S_2017 += dico_2017[filiere][keys]['nb_voeu1']
        Y_2017.append(c_2017)

    for i in range(len(Y_2017)):
        Y_2017[i] = Y_2017[i]/S_2017

    titre = "Evolution de la répartition des voeux de rang 1 entre 2016 et 2017"

    df = pd.DataFrame({'Filières': liste_fil*2, 'Pourcentage de voeux de rang 1': Y_2016 +
                       Y_2017, 'Années': ['2016']*len(Y_2016) + ['2017']*len(Y_2016)})
    fig = px.bar(df, x='Filières', y='Pourcentage de voeux de rang 1',
                 color='Années', barmode='group', title=titre)
    # app.layout = html.Div(children=[
    # html.H1(children='Hello Dash'),

    # html.Div(children='''
    #    Comparaison de la répartition des premiers voeux selon les filières entre 2016 et 2017
    # '''),

    # dcc.Graph(
    # id='example-graph',
    # figure=fig
    # )
    # ])
    return fig


def dash_camembert_filieres_places_disponibles(df):
    """
    dash_camembert_filieres_places_disponibles montre le nombre de places disponibles pour chaque filière

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    Returns
    -------
    un graphe sous forme de camembert
    """
    row = []
    for filiere in liste_filieres(df):
        df_fili = df[df['fili'] == filiere]
        liste_capa = list(df_fili['capa_fin'])
        somme_capa = 0
        for k in range(len(liste_capa)):
            liste_capa[k] = int(liste_capa[k])
            somme_capa += liste_capa[k]
        row.append([filiere, somme_capa])
    liste_f_filiere = [row[i][0] for i in range(len(row))]
    liste_f_capa = [row[i][1] for i in range(len(row))]
    dico_transi = {'filiere': liste_f_filiere,
                   'capacite': liste_f_capa}
    df2 = pd.DataFrame(dico_transi)
    fig = px.pie()
    fig = px.pie(df2, values='capacite', names='filiere',
                 title='Places dans les filières')
    return fig


def dash_camembert_proportion_etablissement_filieres(df):
    """
    dash_camembert_proportion_etablissement_filieres montre le nombre d'établissement proposant de suivre chaque filière

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    Returns
    -------
    un graphe sous forme de camembert
    """
    row = []
    classification = classification_par_filiere(df)
    liste_filiere = []
    liste_nb_etablissement = []
    for filiere in classification.keys():
        liste_filiere.append(filiere)
        nb_etablissement_filiere = len(classification[filiere].keys())
        liste_nb_etablissement.append(nb_etablissement_filiere)

    dico_transi = {'filiere': liste_filiere,
                   'nb_etablissement': liste_nb_etablissement}
    df2 = pd.DataFrame(dico_transi)
    fig = px.pie()
    fig = px.pie(df2, values='nb_etablissement', names='filiere',
                 title="Nombre d'établissement par filière")
    return fig


def dash_camembert_mention_par_etablissement_par_filiere2(df, etablissement, filiere):
    """
    dash_camembert_mention_par_etablissement_par_filiere montre la répartition des mentions dans les élèves admis dans un établissement

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    etablissement: nom de l'établissement
    filiere : filiere étudiée parmi ['1_Licence', '2_DUT', '3_BTS', '4_CPGE', '6_PACES', '7_Management', '8_Ingénieur', 'Autre']

    Returns
    -------
    un graphe sous forme de camembert
    """
    data_temp = df[df['nom_etablissement'] ==
                   etablissement][df['fili'] == filiere]
    dico_temp = data_temp.to_dict('list')
    n = len(dico_temp['sous_filiere'])
    somme_no_mention = 0
    somme_mention_AB = 0
    somme_mention_B = 0
    somme_mention_TB = 0
    for i in range(n):
        somme_no_mention += int(dico_temp['nb_no_mention'][i])
        somme_mention_AB += int(dico_temp['nb_assez_bien'][i])
        somme_mention_B += int(dico_temp['nb_bien'][i])
        somme_mention_TB += int(dico_temp['nb_tres_bien'][i])
    liste_somme = [somme_no_mention, somme_mention_AB,
                   somme_mention_B, somme_mention_TB]

    liste_mention = ['Pas de mention', 'Assez bien', 'Bien', 'Très bien']
    dico_transi = {'mention': liste_mention,
                   'nb_admis_mention': liste_somme}
    df2 = pd.DataFrame(dico_transi)
    fig = px.pie()
    fig = px.pie(df2, values='nb_admis_mention', names='mention',
                 title="Répartition des mentions pour la filière " + filiere + " dans l'établissement " + etablissement)

    return fig


def dash_histogramme_frustration_filieres(df):
    """
    histogramme_frustration_filieres renvoie un histogramme représentant pour chaque filière
    la proportion de candidats ayant accepté une proposition de cette filière qui n'est pas leur premier voeu

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    Returns
    -------
    Un histogramme
    """
    def dico_int(df, l_filieres):
        res = dict()

        for i in l_filieres:
            # on recupere la liste des caractéristiques de cette filière
            l_total_acceptations = list(df[df['fili'] == i]["nb_admis"])
            l_acceptations_voeu1 = list(df[df['fili'] == i]["nb_admis_voe_1"])
            p = len(l_acceptations_voeu1)

            l_total_acceptations_int = [
                int(l_total_acceptations[i]) for i in range(p)]
            l_acceptations_pas_voeu1 = [
                l_total_acceptations_int[i] - int(l_acceptations_voeu1[i]) for i in range(p)]

            # nb_candidats qui n'ont pas eu leur voeu 1
            res[i] = {'nb_acceptes_pas_voeu1': sum(
                l_acceptations_pas_voeu1)/sum(l_total_acceptations_int)}

        return res

    l_filieres = liste_filieres(df)

    res = dico_int(df, l_filieres)

    # Affichage de l'histogramme :
    n = len(l_filieres)

    Valeurs = [res[i]['nb_acceptes_pas_voeu1'] for i in res.keys()]

    # "Proportion d'étudiants acceptés dans un établissement n'étant pas leur premier voeu (par filière respectivement)", fontsize=6)

    df2 = pd.DataFrame({
        "Filières": l_filieres,
        "Taux rapporté au nombre d'étudiants acceptés par filière": Valeurs,
    })

    fig = px.bar(df2, x="Filières", y="Taux rapporté au nombre d'étudiants acceptés par filière",
                 title="Proportion d'étudiants acceptés dans un établissement n'étant pas leur premier voeu (par filière respectivement)")

    return fig


def dash_viz_attractivite(filiere, df, n):
    """
    dash_viz_attractivite renvoie une figure dash en nuage de point du score d'attractivté des n établissements les plus attractifs
    d'une ertaine filière, sous-filière ou filière fine

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille
    filiere : str
        Nom de la filière, sous-filière ou filière fine dont on désire connaître les établissements les plus attractifs
    n : int
        Le nombre de meilleurs établissements qu'on souhaite afficher (on ne les affiche pas tous car le graphique ne serait
        plus lisible)

    Returns
    -------
    Une figure dash
    """

    filiere_cat, y, labels = viz_attractivite(filiere, df, n)

    n = min(n, len(labels))

    df = pd.DataFrame({"Nom de l'établissement": labels,
                       "Indice d'attractivité": y, 'Labels': labels})
    fig = px.scatter(data_frame=df, x="Nom de l'établissement",
                     y="Indice d'attractivité", title='Nuage de point des ' + str(n) + ' établissements les plus attractifs pour la filière ' + filiere_cat)
    return fig


def dash_attractivite_etablissement(etablissement, df, n, type_cat):
    """
    dash_attractivite_etablissement renvoie un graphique dash n filieres ou sous filieres
    ou filieres fines les plus attractives d'un établissement

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille
    filiere : str
        Nom de la filière, sous-filière ou filière fine dont on désire connaître les établissements les plus attractifs
    n : int
        Le nombre de meilleurs établissements qu'on souhaite afficher (on ne les affiche pas tous car le graphique ne serait
        plus lisible)
    etablissement: string
        L'établissement étudié
    type_cat: string
        'filiere' ou 'sous_filiere' ou 'filiere_fine'

    Returns
    -------
    Renvoie une figure dash
    """

    x, y, labels, = attractivite_etablissement(etablissement, df, n, type_cat)

    filiere = ''

    if type_cat == 'filiere':
        filiere = 'filières'
    elif type_cat == 'filiere_fine':
        filiere = 'filières fines'
    elif type_cat == 'sous_filiere':
        filiere = 'sous filières'

    df = pd.DataFrame({filiere: labels,
                       "Indice d'attractivité en %": y})

    fig = px.bar(df, x=filiere, y="Indice d'attractivité en %",
                 title="Indice d'attractivité des " + filiere + " de : " + etablissement)

    return fig


def dash_histogramme_excellence_academique(df, filiere, n):
    """
    Renvoie les n premiers établissements, selon leur proportion d'admis avec la mention très bien

    Parameters
    ----------
    df : dataframe
    filiere : string : filière parmi ['1_Licence', '2_DUT', '3_BTS', '4_CPGE', '6_PACES', '7_Management', '8_Ingénieur', 'Autre']
    n : int : nombre d'établissement à indiquer

    Returns
    -------
    Histogramme sous forme de figure (version dash)
    """
    def tri_rapide_excellence(L):
        if L == []:
            return []
        else:
            pivot = L[0][1]
            L1 = []
            L2 = []
            for x in L[1:]:
                if x[1] > pivot:
                    L1.append(x)
                else:
                    L2.append(x)
            return tri_rapide_excellence(L1) + [L[0]] + tri_rapide_excellence(L2)

    classification = classification_par_filiere(df)
    l_etablissement = classification[filiere].keys()
    l_taux = []
    for etablissement in l_etablissement:
        nb_admis = classification[filiere][etablissement]['nb_admis']
        nb_mention_TB = classification[filiere][etablissement]['nb_tres_bien']
        taux = nb_mention_TB/nb_admis
        l_taux.append([etablissement, taux])
    l_taux_triée = tri_rapide_excellence(l_taux)

    df2 = pd.DataFrame({
        "Etablissement": [l_taux_triée[i][0] for i in range(n)],
        "Taux de mention très bien": [l_taux_triée[i][1] for i in range(n)],
    })
    filiere = filiere[2::]
    fig = px.bar(df2, x="Etablissement", y="Taux de mention très bien",
                 title="Proportion d'étudiants acceptés dans un établissement ayant eu la mention TB pour la filière: " + filiere)

    return fig


def dash_carte_filiere_principale(df):
    """
    dash_carte_filiere_principale renvoie une carte de France colorée selon la filière qui accueille
    le plus d'étudiants pour chaque département


    Parameters
    ----------
    df : dataframe sur lequel on travaille

    Returns
    -------
    une carte de la France
    """

    with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
        departements = json.load(response)
    l_departement = liste_departements(df)
    l_finale = []
    for departement in l_departement:
        l_filiere = liste_filieres(df)
        res = {}
        df2 = df[df['nom_dep'] == departement]
        for filiere in l_filiere:
            l_tempo = list(df2[df2['fili'] == filiere]['nb_admis'])
            somme = 0
            for x in l_tempo:
                somme += int(x)
            res[filiere] = somme
        qte_max = max([res[filiere] for filiere in l_filiere])
        for filiere in l_filiere:
            if res[filiere] == qte_max:
                filiere_max = filiere
        l_finale.append([departement, filiere_max])

    dico_transi = {'nom': [l_finale[i][0] for i in range(len(l_finale))],
                   'filiere_principale': [l_finale[i][1] for i in range(len(l_finale))]}
    df3 = pd.DataFrame(dico_transi)

    fig = px.choropleth_mapbox(df3, geojson=departements, locations='nom', color='filiere_principale', featureidkey='properties.nom',
                               color_continuous_scale="Viridis",
                               range_color=(0, 12),
                               mapbox_style="carto-positron",
                               zoom=5, center={"lat": 46.5132, "lon": 0},
                               opacity=0.5,
                               labels={
                                   'filiere_principale': 'Filière principale'},
                               title="Filière acceuillant le plus d'étudiant dans chaque département"
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def dash_carte_attractivite(df, filiere):
    """
    dash_carte_attractivite renvoie une carte de France colorée selon l'attractivité du département pour
    une filière donnée

    Parameters
    ----------
    df : dataframe sur lequel on travaille
    filiere : str
        nom de la filière, filière fine ou sous-filière pour laquelle on veut avoir les établissements les plus attractifs

    Returns
    -------
    une carte de la France
    """
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

    def indice(df, filiere, etablissement):
        """
        indice renvoie la moyenne des indices de satisfaction calculés pour chaque sous-filière de la filière, filière fine ou
        simplement sous-filière voulue pour un établissement

        calcul de l'indice : 0.4*(0.6*(nb_voeux_1/nb_voeux_tot) - 0.4*((rang_dernier_admis - nb_admis)/nb_voeux_tot))
                                + O.4*pourcentage_admis_tres_bien + 0.2*pourcentage_admis_bien

        Parameters
        ----------
        df : dataframe sur lequel on travaille
        filiere : str
            nom de la filière, filière fine ou sous-filière pour laquelle on veut avoir les établissements les plus attractifs
        etablissement : str
            nom de l'etablissement pour lequel on souhait avoir l'indice

        Returns
        -------
        moy_indice : float
            Moyenne des indices des sous-filières de l'entrée pour l'établissement voulu
        """
        df_2 = df[df['nom_etablissement'] == etablissement]

        # On récupère les listes des valeurs qui nous intéressent pour calculer l'indice d'attractivité : le nombre de voeux 1
        # pour cet établissement, le nombre de voeux totaux, le nombre d'admis, le pourcenatge de mentions bien et de mentions
        # très bien pour les élèves admis dans l'établissement )
        liste_rang_dernier_admis = list(df_2['rang_der_max'])
        liste_voeux_1 = list(df_2['voe1'])
        liste_nb_voeux_tot = list(df_2['voe_tot'])
        liste_nb_admis = list(df_2['nb_admis'])
        liste_p_tres_bien = list(df_2['p_admis_tres_bien'])
        liste_p_bien = list(df_2['p_admis_bien'])
        moy_indice = []

        for i in range(len(liste_nb_admis)):
            # Calcul de l'indice
            indice = 0.9*(int(liste_voeux_1[i])/int(liste_nb_voeux_tot[i])) - 0.1*((int(
                liste_rang_dernier_admis[i])-int(liste_nb_admis[i]))/int(liste_nb_voeux_tot[i]))
            indice = 0.8*indice + 0.15 * \
                liste_p_tres_bien[i] + 0.05*liste_p_bien[i]
            moy_indice.append(float(indice))
        return np.nanmean(moy_indice)
    """
    liste_indice = []
    liste_etablissement = []
    liste_etablissement_rep = []
    df_1 = df
    if filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere':
        df_1 = df[df['fili'] == filiere]

    elif filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere_fine':
        df_1 = df[df['filiere_fine'] == filiere]

    elif filiere_filiere_fine_ou_sous_filiere(filiere) == 'sous_filiere':
        df_1 = df[df['sous_filiere'] == filiere]

    # On obtient la liste de tous les établissements de la filière sans répétition
    liste_etablissement_rep = list(df_1['nom_etablissement'])
    for etablissement in liste_etablissement_rep:
        if etablissement not in liste_etablissement:
            liste_etablissement.append(etablissement)

    # On crée un dictionnaire de la forme {dep_1:[somme des scores, nb d'établissements], dep_2 ...}
    res = {}
    l_departement = liste_departements(df)
    for departement in l_departement:
        res[departement] = [0, 0]
    for etablissement in liste_etablissement:
        departement_selectionne = list(
            df[df["nom_etablissement"] == etablissement]['nom_dep'])[0]
        res[departement_selectionne][0] += indice(df, filiere, etablissement)
        res[departement_selectionne][1] += 1
    l_finale = []
    for departement in res.keys():
        if res[departement][1] != 0:
            moyenne = res[departement][0]/res[departement][1]
        else:
            moyenne = 0
        l_finale.append([departement, moyenne])

    liste_moyenne = [x[1] for x in l_finale]
    valeur_max = max(liste_moyenne)
    """

    l_finale = moy_attractivite_dep(df, filiere)
    liste_moyenne = []
    for i in range(len(l_finale)):
        liste_moyenne.append(l_finale[i][0])
    valeur_max = max(liste_moyenne)
    valeur_min = min(liste_moyenne)

    with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
        departements = json.load(response)

    dico_transi = {'nom': [l_finale[i][1] for i in range(len(l_finale))],
                   'moyenne_attractivite': [l_finale[i][0] for i in range(len(l_finale))]}
    df3 = pd.DataFrame(dico_transi)

    fig = px.choropleth_mapbox(df3, geojson=departements, locations='nom', color='moyenne_attractivite', featureidkey='properties.nom',
                               color_continuous_scale="Viridis",
                               range_color=(valeur_min, valeur_max),
                               mapbox_style="carto-positron",
                               zoom=5, center={"lat": 46.5132, "lon": 0},
                               opacity=0.5,
                               labels={
                                   'moyenne_attractivite': 'Attractivité moyenne'},
                               title="Attractivité moyenne des départements pour la filière :" + filiere
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
