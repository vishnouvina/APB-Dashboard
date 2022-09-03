from data_utils import *
from data_statistics import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def camembert_filieres_places_disponibles(df):
    """
    camembert_filières_places_disponibles renvoie un camembert séparé selon les filières

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    Returns
    -------
    un graphe sous forme de camembert
    """
    dico_temp = capacite_par_filiere(df)
    capacite = {}
    pourcentage = {}
    list_filiere = []
    somme = 0
    for filiere in dico_temp.keys():
        list_filiere.append(filiere)
        capacite[filiere] = dico_temp[filiere]['capacite']
        somme += capacite[filiere]
    for filiere in dico_temp.keys():
        pourcentage[filiere] = capacite[filiere]/somme
    camembert_dico = list(pourcentage.values())
    camembert_labels, camembert_values = [], []
    n = len(camembert_dico)
    for i in range(n):
        camembert_labels.append(list_filiere[i])
        camembert_values.append(camembert_dico[i])

    plt.figure(figsize=(8, 8))
    plt.pie(camembert_values, labels=camembert_labels,
            autopct='%1.1f%%', shadow=False, startangle=90, center=(0, 0), labeldistance=None, pctdistance=1.1)

    plt.title("Répartition des places disponibles",
              fontweight='bold', family='serif')
    plt.axis('equal')
    plt.legend(loc='best')
    plt.show()


def camembert_proportion_etablissement_filieres(df):
    """
    camembert_proportion_etablissement_filières renvoie un camembert séparé selon les filières

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    Returns
    -------
    un graphe sous forme de camembert
    """
    dico_temp = classification_par_filiere(df)
    nb_etablissement = {}
    pourcentage = {}
    list_filiere = []
    somme = 0
    for filiere in dico_temp.keys():
        list_filiere.append(filiere)
        nb_etablissement[filiere] = len(dico_temp[filiere].keys())
        somme += nb_etablissement[filiere]
    for filiere in dico_temp.keys():
        pourcentage[filiere] = nb_etablissement[filiere]/somme
    camembert_dico = list(pourcentage.values())
    camembert_labels, camembert_values = [], []
    n = len(camembert_dico)
    for i in range(n):
        camembert_labels.append(list_filiere[i])
        camembert_values.append(camembert_dico[i])

    plt.figure(figsize=(8, 8))
    plt.pie(camembert_values, labels=camembert_labels,
            autopct='%1.1f%%', shadow=False, startangle=90, center=(0, 0), labeldistance=None, pctdistance=1.1)

    plt.title("Répartition du nombre d'établissement",
              fontweight='bold', family='serif')
    plt.axis('equal')
    plt.legend(loc='best')
    plt.show()


def histogramme_taux_critere_par_filiere(df2016, df2017, critere='fille'):
    """
    histogramme_taux_critere_par_filiere renvoie un histogramme montrant l'évolution du taux de personnes répondant à un critère dans les différentes filières entre 2016 et 2017

    Parameters
    ----------
    df2016: le dataframe de 2016 sur lequel on travaille

    df2017: le dataframe de 2017 sur lequel on travaille

    critere: str
        le critère qu'on veut sélectionner, par défaut c'est "être une femme".
        Les choix disponibles sont "boursier" et "fille"

    Returns
    -------
    Un histogramme
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

    # Ici, liste_taux_filles contient les taux de filles dans les différentes filières
    # Et filieres contient ces filières en question

    # Affichage de l'histogramme :
    width = 0.4
    b2016 = plt.bar(range(n), liste_taux_critere1, width=width, color='red')
    b2017 = plt.bar([i + width for i in range(n)],
                    liste_taux_critere2, width=width, color='blue')
    plt.xticks([i + width/2 for i in range(n)], filieres, rotation=30)

    if critere == 'fille':
        plt.legend([b2016, b2017], [
            'taux de filles en 2016', 'taux de filles en 2017'])
        plt.title(
            "Evolution du taux de filles dans les différentes filières entre 2016 et 2017")
        plt.ylabel("Taux de filles")
    elif critere == 'boursier':
        plt.legend([b2016, b2017], [
            'taux de boursiers en 2016', 'taux de boursiers en 2017'])
        plt.title(
            "Evolution du taux de boursiers dans les différentes filières entre 2016 et 2017")
        plt.ylabel("Taux de boursiers")

    plt.tight_layout()
    plt.show()


def histogramme_taux_critere_par_sous_filiere(df2016, df2017, liste_filieres, critere='fille'):
    """
    histogramme_taux_critere_par_filiere renvoie un histogramme montrant l'évolution du taux de filles dans les différentes filières entre 2016 et 2017

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
    Un histogramme
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
                liste_taux_critere.append()

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
    width = 0.4
    b2016 = plt.bar(range(n), liste_taux_critere1, width=width, color='red')
    b2017 = plt.bar([i + width for i in range(n)],
                    liste_taux_critere2, width=width, color='blue')
    plt.xticks([i + width/2 for i in range(n)],
               filieres, rotation=45, fontsize=6)

    if critere == 'fille':
        plt.legend([b2016, b2017], [
            'taux de filles en 2016', 'taux de filles en 2017'])
        plt.title(
            "Evolution du taux de filles dans les différentes filières entre 2016 et 2017")
        plt.ylabel("Taux de filles")
    elif critere == 'boursier':
        plt.legend([b2016, b2017], [
            'taux de boursiers en 2016', 'taux de boursiers en 2017'])
        plt.title(
            "Evolution du taux de boursiers dans les différentes filières entre 2016 et 2017")
        plt.ylabel("Taux de boursiers")

    plt.tight_layout()
    plt.show()


def histo_plus_demande(df):
    """
    histo_plus_demande renvoie le graphique montrant la répartition des voeux de rang 1 selon les différentes
    filières.

    Parameters
    ----------
    df : le dataframe sur lequel on travaille

    Returns
    -------
    Un graphique sous forme d'histogramme ou de camembert (à définir)

    """
    liste_fil = liste_filieres(df)
    dico = classification_par_filiere(df)
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
    # plt.pie(Y, labels=liste_fil, autopct=lambda x: str(
        # round(x, 2)) + '%', pctdistance=0.5)
    plt.title('Répartition des premiers voeux selon les filières')
    plt.bar(liste_fil, Y, width=0.7)
    plt.xticks(rotation=30)
    plt.show()


def histogramme_refus_filiere(df):
    """
    histogramme_refus_filieres renvoie un histogramme représentant pour chaque filière
    la juxtaposition du nb de candidats, de personnes acceptées et de personnes qui ont validé

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    Returns
    -------
    Un histogramme
    """

    res = voeux_propositions_acceptations(df)
    l_filieres = liste_filieres(df)

    # Affichage de l'histogramme :
    n = len(l_filieres)

    width = 0.3

    capa_filieres = capacite_par_filiere(df)

    l_c = [int(res[i]['nb_candidatures'])/int(capa_filieres[i]['capacite'])
           for i in res.keys()]
    l_p = [int(res[i]['nb_propositions'])/int(capa_filieres[i]['capacite'])
           for i in res.keys()]
    l_a = [int(res[i]['nb_acceptations'])/int(capa_filieres[i]['capacite'])
           for i in res.keys()]
    c = plt.bar(range(n), l_c, width=width, color='red')
    p = plt.bar([i + width for i in range(n)], l_p, width=width, color='blue')
    a = plt.bar([i + 2*width for i in range(n)],
                l_a, width=width, color='green')

    plt.xticks([i + width/3 for i in range(n)], l_filieres, rotation=30)

    plt.legend([c, p, a], ["Nombre de candidatures",
                           "Nombres de propositions", "Nombres d'acceptations"])
    plt.title(
        "Répartition des filières engendrant le plus de refus par rapport à leur capacité")
    plt.ylabel("Taux rapportés à la capacité de chaque filière")

    plt.tight_layout()
    plt.show()


def histogramme_refus_sous_filiere(df, l_filieres):
    """
    histogramme_refus_filieres_fines renvoie un histogramme représentant pour chaque fsous filiere choisie
    la juxtaposition du nb de candidats, de personnes acceptées et de personnes qui ont validé

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    l_filieres: la liste des filieres desquelles on veut extraire les sous filieres
    Returns
    -------
    Un histogramme
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

    width = 0.3
    capa_sous_filieres = capacite_par_sous_filiere(df, l_filieres)

    l_c = [int(res[i]['nb_candidatures']) /
           int(capa_sous_filieres[i]['capacite']) for i in res.keys()]
    l_p = [int(res[i]['nb_propositions']) /
           int(capa_sous_filieres[i]['capacite']) for i in res.keys()]
    l_a = [int(res[i]['nb_acceptations']) /
           int(capa_sous_filieres[i]['capacite']) for i in res.keys()]

    c = plt.bar(range(n), l_c, width=width, color='red')
    p = plt.bar([i + width for i in range(n)], l_p, width=width, color='blue')
    a = plt.bar([i + 2*width for i in range(n)],
                l_a, width=width, color='green')

    plt.xticks([i + width/3 for i in range(n)], l_sous_filieres, rotation=30)

    plt.legend([c, p, a], ["Nombre de candidatures",
                           "Nombres de propositions", "Nombres d'acceptations"])
    plt.title(
        "Répartition des filières engendrant le plus de refus par rapport à leur capacité")
    plt.ylabel("Taux rapportés à la capacité de chaque filière")

    plt.tight_layout()
    plt.show()


def camembert_mention_par_etablissement_par_filiere(df, etablissement, filiere):
    """
    camembert_mention_par_etablissement_par_filiere montre la répartition des mentions dans les élèves admis dans un établissement

    Parameters
    ----------
    df: le dataframe sur lequel on travaille
    etablissement: nom de l'établissement
    filiere : filiere étudiée parmi ['1_Licence', '2_DUT', '3_BTS', '4_CPGE', '6_PACES', '7_Management', '8_Ingénieur', 'Autre']

    Returns
    -------
    un graphe sous forme de camembert
    """
    dico_temp = df[df['nom_etablissement'] ==
                   etablissement][df['fili'] == filiere].to_dict('list')
    n = len(dico_temp['sous_filiere'])
    somme_eleve = 0
    somme_no_mention = 0
    somme_mention_AB = 0
    somme_mention_B = 0
    somme_mention_TB = 0
    for i in range(n):
        somme_no_mention += int(dico_temp['nb_no_mention'][i])
        somme_mention_AB += int(dico_temp['nb_assez_bien'][i])
        somme_mention_B += int(dico_temp['nb_bien'][i])
        somme_mention_TB += int(dico_temp['nb_tres_bien'][i])
        somme_eleve += int(dico_temp['nb_admis'][i])
    liste_somme = [somme_no_mention/somme_eleve, somme_mention_AB /
                   somme_eleve, somme_mention_B/somme_eleve, somme_mention_TB/somme_eleve]

    liste_mention = ['Pas de mention', 'Assez bien', 'Bien', 'Très bien']
    plt.figure(figsize=(8, 8))
    plt.pie(liste_somme, labels=liste_mention,
            autopct='%1.1f%%', shadow=False, startangle=90, center=(0, 0), labeldistance=None, pctdistance=1.1)

    plt.title("Répartition des mentions pour la filière " + filiere + "dans l'établissement " + etablissement,
              fontweight='bold', family='serif')
    plt.axis('equal')
    plt.legend(loc='best')
    plt.show()


def histo_plus_demande_annees(df2016, df2017):
    """
    Renvoie l'évolution de la répartition des voeux de rang1 entre 2016 et 2017

    Parameters
    ----------
    df2016 : dataframe de 2016
    df2017 : dataframe de 2017

    Returns
    -------
    Graphique sous forme d'histogrammes
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

    barWidth = 0.4
    r1 = range(len(Y_2016))
    r2 = [x+barWidth for x in r1]
    plt.title('Comparaison de la répartition des premiers voeux selon les filières')
    plt.bar(r1, Y_2016, width=barWidth, color=['yellow' for i in Y_2016])
    plt.bar(r2, Y_2017, width=barWidth, color=['pink' for i in Y_2016])
    plt.xticks([r + barWidth / 2 for r in range(len(Y_2016))],
               liste_fil, rotation=30)
    b1 = plt.bar(range(1), [0], width=0.4, color='yellow')
    b2 = plt.bar([x + 0.4 for x in range(1)], [0], width=0.4, color='pink')
    plt.legend([b1, b2], ['2016', '2017'])
    plt.show()


def histogramme_frustration_filieres(df):
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

    width = 0.3

    l_c = [res[i]['nb_acceptes_pas_voeu1'] for i in res.keys()]

    c = plt.bar(range(n), l_c, width=width, color='green')

    plt.xticks([i for i in range(n)], l_filieres, rotation=30)

    plt.title("Proportion d'étudiants acceptés dans un établissement n'étant pas leur premier voeu (par filière respectivement)", fontsize=6)
    plt.ylabel(
        "Taux rapporté au nombre d'étudiants accepté respectivement dans chaque filière", fontsize=6)

    plt.tight_layout()
    plt.show()


def comparaison_filles_admises_parfiliere(df2016, df2017):
    """
    renvoie l'évolution du nombre d'admises par filière entre 2016 et 2017

    Parameters
    ----------
    df2016 : dataframe de 2016
    df2017 : dataframe de 2017

    Returns
    -------
    Graphique sous forme d'histogrammes
    """

    dico_2016 = classification_par_filiere(df2016)
    dico_2017 = classification_par_filiere(df2017)
    liste_fil = liste_filieres(df2016)
    Y_2016 = []
    Y_2017 = []
    for filiere in liste_fil:
        c_2016 = 0  # le nombre d'admises pour une filière
        for keys in dico_2016[filiere]:
            c_2016 += dico_2016[filiere][keys]['nb_admis_voeu1_f']
        Y_2016.append(c_2016)
    for filiere in liste_fil:
        c_2017 = 0  # le nombre d'admises pour une filière
        for keys in dico_2017[filiere]:
            c_2017 += dico_2017[filiere][keys]['nb_admis_voeu1_f']
        Y_2017.append(c_2017)

    barWidth = 0.4
    r1 = range(len(Y_2016))
    r2 = [x+barWidth for x in r1]
    plt.title('Comparaison du nombre d\' étudiantes admises par filière')
    plt.bar(r1, Y_2016, width=barWidth, color=['purple' for i in Y_2016])
    plt.bar(r2, Y_2017, width=barWidth, color=['pink' for i in Y_2016])
    plt.xticks([r + barWidth / 2 for r in range(len(Y_2016))],
               liste_fil, rotation=30)
    b1 = plt.bar(range(1), [0], width=0.4, color='purple')
    b2 = plt.bar([x + 0.4 for x in range(1)], [0], width=0.4, color='pink')
    plt.legend([b1, b2], ['2016', '2017'])
    plt.xticks(rotation=30)
    plt.show()


def viz_attractivite(filiere, df, n):
    """
    viz_attractivite renvoie un graphique en nuage de point du score d'attractivté des n établissements les plus attractifs
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
    Les listes pour réaliser un graph dash
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

        calcul de l'indice : 0.8*(0.9*(nb_voeux_1/nb_voeux_tot) - 0.1*((rang_dernier_admis - nb_admis)/nb_voeux_tot))
                                + O.15*pourcentage_admis_tres_bien + 0.05*pourcentage_admis_bien

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

    # On met chaque couple [moyenne des indices de l'établissment, nom de l'établissement] dans une liste qu'on trie
    # de manière croissante
    for etablissement in liste_etablissement:
        liste_indice.append(
            [indice(df, filiere, etablissement), etablissement])
    liste_indice.sort()

    # Construction du graphique
    if filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere':
        filiere = filiere[2::]

    labels = []
    y = []
    x = []
    n = min(len(liste_indice), n)
    for i in range(n):
        y.append(liste_indice[-(i+1)][0])
        labels.append(liste_indice[-(i+1)][1])
        x.append(i)
    
    def distribution_probas(y):
        """
        distribution_probas prend en entrée un vecteur y de nombres et renvoie une distribution de probas
        """
        p = len(y)
        S = 0
        for i in range(p):
            S += y[i]
        for i in range(p):
            y[i] = y[i]/S
        return y

    y = distribution_probas(y)
    return filiere, y, labels


def attractivite_etablissement(etablissement, df, n, type_cat):
    """
    attractivite_etablissement renvoie un graphique en nuage de point des  n filieres ou sous filieres 
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
    Renvoie listes pour créer graph dash
    """

    def tri_ins(t):
        if len(t) > 1:
            for k in range(1, len(t)):
                temp = t[k]
                j = k
            while j > 0 and temp[0] < t[j-1][0]:
                t[j] = t[j-1]
                j -= 1
                t[j] = temp
        return t

    def indice_etablissement(etablissement, type_cat,  df):
        dico = {}
        liste_indice = []
        if type_cat == 'filiere':
            dico = classification_par_filiere(df)
        elif type_cat == 'filiere_fine':
            liste_filiere = liste_filieres(df)
            dico = classification_par_filiere_fine(df, liste_filiere)
        elif type_cat == 'sous_filiere':
            liste_filiere = liste_filieres(df)
            dico = classification_par_sous_filiere(df, liste_filiere)
        for filiere in dico.keys():
            if etablissement in dico[filiere]:
                if type_cat == 'filiere':
                    df_2 = df[df['fili'] ==
                              filiere][df['nom_etablissement'] == etablissement]
                elif type_cat == 'filiere_fine':
                    df_2 = df[df['filiere_fine'] ==
                              filiere][df['nom_etablissement'] == etablissement]
                elif type_cat == 'sous_filiere':
                    df_2 = df[df['sous_filiere'] ==
                              filiere][df['nom_etablissement'] == etablissement]
                liste_nb_voeu = list(df_2['voe_tot'])
                for i in range(len(liste_nb_voeu)):
                    liste_nb_voeu[i] = int(liste_nb_voeu[i])
                nb_voeux_tot = sum(liste_nb_voeu)
                indice = dico[filiere][etablissement]["nb_voeu1"]/nb_voeux_tot
                indice = 0.7*indice + 0.2*(dico[filiere][etablissement]['nb_tres_bien']/dico[filiere][etablissement]['nb_admis']) + 0.1*(
                    dico[filiere][etablissement]['nb_bien']/dico[filiere][etablissement]['nb_admis'])
                liste_indice.append([indice, filiere])
        return liste_indice

    liste_indice = indice_etablissement(etablissement, type_cat, df)
    tri_ins(liste_indice)
    n = min(n, len(liste_indice))
    y = []
    labels = []
    for i in range(n):
        y.append(liste_indice[-(i+1)][0])
        labels.append(liste_indice[-(i+1)][1])
    
    def distribution_probas(y):
        """
        distribution_probas prend en entrée un vecteur y de nombres et renvoie une distribution de probas
        """
        p = len(y)
        S = 0
        for i in range(p):
            S += y[i]
        for i in range(p):
            y[i] = (y[i]/S)*100
        return y

    y = distribution_probas(y)
    x = [i for i in range(n)]
    return x, y, labels

