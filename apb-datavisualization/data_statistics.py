from data_utils import *
import pandas as pd
import numpy as np


def liste_regions(df):
    """
    liste_regions renvoie la liste des différentes régions présentes sur le dataframe

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille


    Returns
    -------
    list : [region1, region2, ...]
    """

    L = list(df['nom_reg'])
    L2 = [L[0]]
    for region in L:
        if region not in L2:
            L2.append(region)
    return L2


def liste_departements(df):
    """
    liste_departements renvoie la liste des différents départements présentes sur le dataframe

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille


    Returns
    -------
    list : [departement1, departement2, ...]
    """

    L = list(df['nom_dep'])
    L2 = [L[0]]
    for dep in L:
        if dep not in L2:
            L2.append(dep)
    return L2


def liste_sous_filiere(df, filiere):
    """
    liste_sous_filiere renvoie la liste des sous-filières d'une filière présente sur le dataframe
    (par exemple, les sous-filières de CPGE sont MPSI, PCSI, TSI...)

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille
    filiere : str
        Nom de la filière dont on veut connaitre les sous filieres

    Returns
    -------
    list : [sous_filiere1, sous_filiere2, ...]
    (ou None si la filière n'existe pas)
    """

    df_fili = df[df['fili'] == filiere]
    L = list(df_fili['sous_filiere'])

    if (len(L) == 0):
        return None

    else:
        L2 = [L[0]]
        for sousfili in L:
            if sousfili not in L2:
                L2.append(sousfili)
        return L2


def liste_filieres(dataframe):
    """
    liste_filieres renvoie la liste des différentes filières présentes sur le dataframe

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille


    Returns
    -------
    list : [filiere1, filiere2, ...]
    """

    return ['1_Licence', '2_DUT', '3_BTS', '4_CPGE', '6_PACES', '7_Management', '8_Ingénieur', 'Autre']


def liste_filieres_fines(df, filiere):
    """
    liste_filiere_fine renvoie la liste des filières fines d'une filière présente sur le dataframe
    (par exemple, les filières fines de CPGE sont Classe préparatoire scientifique, Classe préparatoire littéraire, ...

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille
    filiere : str
        Nom de la filière dont on veut connaitre les filieres fines

    Returns
    -------
    list : [filiere_fine1, filiere_fine2, ...]
    (ou None si la filière n'existe pas)
    """

    df_fili = df[df['fili'] == filiere]
    L = list(df_fili['filiere_fine'])

    if (len(L) == 0):
        return None

    else:
        L2 = [L[0]]
        for sousfili in L:
            if sousfili not in L2:
                L2.append(sousfili)
        return L2


def separation_dataframe_par_region(df, region):
    """
    separation_dataframe_par_region charge une dataframe et la renvoie tronquée,
    en ne gardant que les établissements de la région

    Parameters
    ----------
    df : dataframe
        tableau original à tronquer

    region : str
        nom de la région sélectionnée

    Returns
    -------
    df_region : dataframe
        dataframe tronquée selon la région
    """

    df_region = df[df['nom_reg'] == region]
    return df_region.reset_index(drop=True)


def separation_dataframe_par_departement(df, departement):
    """
    separation_dataframe_par_département charge une dataframe et la renvoie tronquée,
    en ne gardant que les établissements du département

    Parameters
    ----------
    df : dataframe
        tableau original à tronquer

    region : str
        nom du département sélectionné

    Returns
    -------
    df_departement : dataframe
        dataframe tronquée selon le département
    """
    df_departement = df[df['nom_dep'] == departement]
    return df_departement.reset_index(drop=True)


def classification_par_filiere(dataframe):  # filiere : cpge, etc
    """
    classification_par_filiere renvoie un dicitonnaire organisé par filière

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    Returns
    -------
    { filiere1 : { lycée1 : {capacité : , rang_dernier_admis: , nombre_mentions_tb: , ... },

                   lycée2 : { … },

                 },

      filiere2 : { lycée1 : { … } ,

                   lycée2 : { … },

                 },
    }
    """

    # Initialisation de la forme du résultat
    res = dict()
    filieres = liste_filieres(dataframe)
    nb_filieres = len(filieres)
    for i in range(nb_filieres):
        res[filieres[i]] = {}
    # Ici, on a res = {filiere1 : {} , filiere2 : {} , ...}

    # On charge toutes les colonnes du dataset dont on a besoin
    fili = dataframe['fili']
    nom_etab = dataframe['nom_etablissement']
    capacite = dataframe['capa_fin']
    nb_admis = dataframe['nb_admis']
    nb_admis_f = dataframe['nb_admis_f']
    nb_admis_voeu1 = dataframe['nb_admis_voe_1']
    nb_admis_voeu1_f = dataframe['nb_admis_voe1_f']
    nb_boursiers = dataframe['nb_boursiers']
    nb_tres_bien = dataframe['nb_tres_bien']
    nb_bien = dataframe['nb_bien']
    nb_assez_bien = dataframe['nb_assez_bien']
    nb_no_mention = dataframe['nb_no_mention']
    nb_voeu1 = dataframe['voe1']
    nb_voeu1_f = dataframe['voe1_f']

    # On remplit alors le dictionnaire résultat
    n = len(fili)
    for i in range(n):
        # Pour chaque école du dataframe
        if fili[i] in filieres:
            # Si l'établissement a pas encore été pris en compte pour cette filière (par exemple dans le cas où l'établissement a plusieurs sous filieres)
            if (nom_etab[i] not in res[fili[i]].keys()):
                res[fili[i]][nom_etab[i]] = {'capacite': int(capacite[i]), 'nb_admis': int(nb_admis[i]), 'nb_admis_f': int(nb_admis_f[i]), 'nb_admis_voeu1': int(nb_admis_voeu1[i]),
                                             'nb_admis_voeu1_f': int(nb_admis_voeu1_f[i]), 'nb_boursiers': int(nb_boursiers[i]), 'nb_tres_bien': int(nb_tres_bien[i]),
                                             'nb_bien': int(nb_bien[i]), 'nb_assez_bien': int(nb_assez_bien[i]), 'nb_no_mention': int(nb_no_mention[i]),
                                             'nb_voeu1': int(nb_voeu1[i]), 'nb_voeu1_f': int(nb_voeu1_f[i])}

            else:  # Sinon, ie si l'établissement a déjà été pris en compte
                a = res[fili[i]][nom_etab[i]]
                a['capacite'] += int(capacite[i])
                a['nb_admis'] += int(nb_admis[i])
                a['nb_admis_f'] += int(nb_admis_f[i])
                a['nb_admis_voeu1'] += int(nb_admis_voeu1[i])
                a['nb_boursiers'] += int(nb_boursiers[i])
                a['nb_tres_bien'] += int(nb_tres_bien[i])
                a['nb_bien'] += int(nb_bien[i])
                a['nb_assez_bien'] += int(nb_assez_bien[i])
                a['nb_no_mention'] += int(nb_no_mention[i])
                a['nb_voeu1'] += int(nb_voeu1[i])
                a['nb_voeu1_f'] += int(nb_voeu1_f[i])

    return res


def capacite_par_filiere(df):
    """
    capacite_par_filiere renvoie un dicitonnaire organisé par filière

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    Returns
    -------
    { filiere1 : { capacite: int, proportion: float },
      filiere2 : { capacite: int, proportion: float },
      ... }
    """

    res = dict()
    l_filieres = liste_filieres(df)
    compteur_total = 0

    for i in l_filieres:
        # on recupere la liste des etablissements de cette filiere
        l = list(df[df['fili'] == i]["capa_fin"])
        l_int = [int(l[i]) for i in range(len(l))]
        # cette liste contient les capacités de chaque établissement de la filiere
        res[i] = {'capacite': sum(l_int)}
        compteur_total += sum(l_int)

    for i in l_filieres:
        if (compteur_total == 0):
            res[i]['proportion'] = 0
        else:
            res[i]['proportion'] = res[i]['capacite']/compteur_total
    return res


def demande_voeu1_par_filiere(dataframe):
    """
    demande_par_filiere renvoie un dicitonnaire organisé par filière, avec pour chaque filière
    le nombre de demandes en voeu 1 et la proportion que cela représente

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    Returns
    -------
    { filiere1 : { demande: int, proportion_demande: float, nb_filles: int },
      filiere2 : { demande: int, proportion_demande: float, nb_filles: int },
      ... }
    """

    def sommation(d, filiere, categorie):
        """
        Parameters
        ----------
        d: dict
            Dictionnaire retourné par classification_par_filiere

        filiere: str
            Filiere dont on veut les statistiques (par exemple, "1_Licence", ou ("4_CPGE"))

        categorie: str
            Catégorie qu'on veut récuperer sur la filière en question (par exemple le nombre d'élèves
            qui ont mis l'école en voeu 1 (nb_voeu1))

        Returns
        -------
        compteur: int
        """

        capacite = 0

        for lycee in d[filiere].keys():
            nombre = d[filiere][lycee][categorie]
            if nombre != 'inconnu':
                nombre = int(nombre)
                capacite += nombre
        return capacite

    # On initialise le dictionnaire qui contient les informations pour chaque filière, et le dictionnaire résultat
    d = classification_par_filiere(dataframe)
    res = dict()
    l_filieres = liste_filieres(dataframe)  # Liste des filières du dataframe
    compteur_total_nb_voeu1 = 0

    for filiere in l_filieres:
        # Pour chaque filière

        # On compte le nombre de voeu1 pour chaque filière, le nombre de filles qui ont mis voeu 1, le nombre de boursiers, etc
        # nombre d'élèves qui ont mis cette filière en voeu 1
        compteur_nb_voeu1 = sommation(d, filiere, 'nb_voeu1')
        compteur_total_nb_voeu1 += compteur_nb_voeu1
        compteur_nb_filles = sommation(d, filiere, 'nb_voeu1_f')

        # On initialise res[filiere]
        res[filiere] = {'demande': compteur_nb_voeu1}
        res[filiere]['nb_filles'] = compteur_nb_filles
        # res[filiere['nb_boursiers']] = compteur_nb_boursiers

    # On remplit ensuite les proportions pour le nombre de demandes
    for filiere in l_filieres:
        if (compteur_total_nb_voeu1 == 0):
            res[filiere]['proportion_demande'] = 0
        else:
            res[filiere]['proportion_demande'] = res[filiere]['demande'] / \
                compteur_total_nb_voeu1

    return res


def classification_par_sous_filiere(dataframe, liste_filiere):
    """
    classification_par_sous_filiere renvoie un dicitonnaire organisé par sous filières

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    liste_filiere: list
            Liste de filières dont on veut extraire les sous filières
            (par exemple : liste_filiere = ['3_BTS', '4_CPGE'])

    Returns
    -------
    { sous_filiere1 : { lycée1 : {capacité : , rang_dernier_admis: , nombre_mentions_tb: , ... },

                   lycée2 : { … },

                 },

      sous_filiere2 : { lycée1 : { … } ,

                   lycée2 : { … },

                 },
    }
    """

    # Initialisation de la forme du résultat
    res = dict()

    # On crée la liste des filières fines qu'on va considérer
    filieres = []
    for i in range(len(liste_filiere)):
        filieres += liste_sous_filiere(dataframe, liste_filiere[i])
    nb_filieres = len(filieres)
    for i in range(nb_filieres):
        res[filieres[i]] = {}
    # Ici, on a res = {sous_filiere1 : {} , sous_filiere2 : {} , ...}

    # On charge toutes les colonnes du dataset dont on a besoin
    sous_fili = dataframe['sous_filiere']
    nom_etab = dataframe['nom_etablissement']
    capacite = dataframe['capa_fin']
    nb_admis = dataframe['nb_admis']
    nb_admis_f = dataframe['nb_admis_f']
    nb_admis_voeu1 = dataframe['nb_admis_voe_1']
    nb_admis_voeu1_f = dataframe['nb_admis_voe1_f']
    nb_boursiers = dataframe['nb_boursiers']
    nb_tres_bien = dataframe['nb_tres_bien']
    nb_bien = dataframe['nb_bien']
    nb_assez_bien = dataframe['nb_assez_bien']
    nb_no_mention = dataframe['nb_no_mention']
    nb_voeu1 = dataframe['voe1']
    nb_voeu1_f = dataframe['voe1_f']

    # On remplit alors le dictionnaire résultat
    n = len(sous_fili)
    for i in range(n):
        # Pour chaque école du dataframe
        if sous_fili[i] in filieres:
            # Si l'établissement a pas encore été pris en compte pour cette filière (par exemple dans le cas où l'établissement a plusieurs sous filieres)
            if (nom_etab[i] not in res[sous_fili[i]].keys()):
                res[sous_fili[i]][nom_etab[i]] = {'capacite': int(capacite[i]), 'nb_admis': int(nb_admis[i]), 'nb_admis_f': int(nb_admis_f[i]), 'nb_admis_voeu1': int(nb_admis_voeu1[i]),
                                                  'nb_admis_voeu1_f': int(nb_admis_voeu1_f[i]), 'nb_boursiers': int(nb_boursiers[i]), 'nb_tres_bien': int(nb_tres_bien[i]),
                                                  'nb_bien': int(nb_bien[i]), 'nb_assez_bien': int(nb_assez_bien[i]), 'nb_no_mention': int(nb_no_mention[i]),
                                                  'nb_voeu1': int(nb_voeu1[i]), 'nb_voeu1_f': int(nb_voeu1_f[i])}

            else:  # Sinon, ie si l'établissement a déjà été pris en compte
                a = res[sous_fili[i]][nom_etab[i]]
                a['capacite'] += int(capacite[i])
                a['nb_admis'] += int(nb_admis[i])
                a['nb_admis_f'] += int(nb_admis_f[i])
                a['nb_admis_voeu1'] += int(nb_admis_voeu1[i])
                a['nb_boursiers'] += int(nb_boursiers[i])
                a['nb_tres_bien'] += int(nb_tres_bien[i])
                a['nb_bien'] += int(nb_bien[i])
                a['nb_assez_bien'] += int(nb_assez_bien[i])
                a['nb_no_mention'] += int(nb_no_mention[i])
                a['nb_voeu1'] += int(nb_voeu1[i])
                a['nb_voeu1_f'] += int(nb_voeu1_f[i])

    return res


def capacite_par_sous_filiere(dataframe, liste_filiere):
    """
    capacite_par_sous_filiere renvoie un dictonnaire organisé par sous filières

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    liste_filiere: list
            Liste de filières dont on veut extraire les sous filières
            (par exemple : liste_filiere = ['3_BTS', '4_CPGE'])

    Returns
    -------
    { sous_filiere1 : { capacite: int, proportion: float },
      sous_filiere2 : { capacite: int, proportion: float },
      ... }
    """

    def compteur_capacite(d, filiere):
        capacite = 0

        for i in d[filiere].keys():
            a = d[filiere][i]['capacite']
            if a != 'inconnu':
                a = int(a)
                capacite += a
        return capacite

    d = classification_par_sous_filiere(dataframe, liste_filiere)

    res = dict()
    l_filieres = []
    for i in range(len(liste_filiere)):
        l_filieres += liste_sous_filiere(dataframe, liste_filiere[i])

    compteur_total = 0
    for i in l_filieres:
        compteur = compteur_capacite(d, i)
        compteur_total += compteur
        res[i] = {'capacite': compteur}
    for i in l_filieres:
        if (compteur_total == 0):
            res[i]['proportion'] = 0
        else:
            res[i]['proportion'] = res[i]['capacite']/compteur_total

    return res


def capacite_par_filiere_fine(dataframe, liste_filiere):
    """
    capacite_par_filiere_fine renvoie un dictonnaire organisé par filieres fines

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    liste_filiere: list
            Liste de filières dont on veut extraire les filieres fines
            (par exemple : liste_filiere = ['3_BTS', '4_CPGE'])

    Returns
    -------
    { filiere_fine1 : { capacite: int, proportion: float },
      filiere_fine2 : { capacite: int, proportion: float },
      ... }
    """

    def compteur_capacite(d, filiere):
        capacite = 0

        for i in d[filiere].keys():
            a = d[filiere][i]['capacite']
            if a != 'inconnu':
                a = int(a)
                capacite += a
        return capacite

    d = classification_par_filiere_fine(dataframe, liste_filiere)

    res = dict()
    l_filieres = []
    for i in range(len(liste_filiere)):
        l_filieres += liste_filieres_fines(dataframe, liste_filiere[i])

    compteur_total = 0
    for i in l_filieres:
        compteur = compteur_capacite(d, i)
        compteur_total += compteur
        res[i] = {'capacite': compteur}
    for i in l_filieres:
        if (compteur_total == 0):
            res[i]['proportion'] = 0
        else:
            res[i]['proportion'] = res[i]['capacite']/compteur_total

    return res


def demande_voeu1_par_sous_filiere(dataframe, liste_filiere):
    def sommation(d, filiere, categorie):
        """
        demande_par_sous_filiere renvoie un dicitonnaire organisé par filières fines, avec pour chaque
        filière fine le nombre de demandes en voeu 1 et la proportion que cela représente

        Parameters
        ----------
        dataframe: le dataframe sur lequel on travaille

        liste_filiere: list
            Liste de filières dont on veut extraire les sous filières
            (par exemple : liste_filiere = ['3_BTS', '4_CPGE'])

        Returns
        -------
        { sous_filiere1 : { demande: int, proportion_demande: float, nb_filles: int },
          sous_filiere2 : { demande: int, proportion_demande: float, nb_filles: int },
        ... }
        """

        capacite = 0

        for lycee in d[filiere].keys():
            nombre = d[filiere][lycee][categorie]
            if nombre != 'inconnu':
                nombre = int(nombre)
                capacite += nombre
        return capacite

    # On initialise le dictionnaire qui contient les informations pour chaque filière, et le dictionnaire résultat
    d = classification_par_sous_filiere(dataframe, liste_filiere)
    res = dict()

    l_filieres = []  # Liste des filières du dataframe
    for i in range(len(liste_filiere)):
        l_filieres += liste_sous_filiere(dataframe, liste_filiere[i])
    compteur_total_nb_voeu1 = 0

    for filiere in l_filieres:
        # Pour chaque filière

        # On compte le nombre de voeu1 pour chaque filière, le nombre de filles qui ont mis voeu 1, le nombre de boursiers, etc
        # nombre d'élèves qui ont mis cette filière en voeu 1
        compteur_nb_voeu1 = sommation(d, filiere, 'nb_voeu1')
        compteur_total_nb_voeu1 += compteur_nb_voeu1
        compteur_nb_filles = sommation(d, filiere, 'nb_voeu1_f')

        # On initialise res[filiere]
        res[filiere] = {'demande': compteur_nb_voeu1}
        res[filiere]['nb_filles'] = compteur_nb_filles
        # res[filiere['nb_boursiers']] = compteur_nb_boursiers

    # On remplit ensuite les proportions pour le nombre de demandes
    for filiere in l_filieres:
        if (compteur_total_nb_voeu1 == 0):
            res[filiere]['proportion_demande'] = 0
        else:
            res[filiere]['proportion_demande'] = res[filiere]['demande'] / \
                compteur_total_nb_voeu1

    return res


def voeux_propositions_acceptations(df):
    """
    voeux_propositions_acceptations renvoie un dico représentant pour chaque filière
    le nb total de candidats, de personnes acceptées et de personnes qui ont validé

    Parameters
    ----------
    df: le dataframe sur lequel on travaille

    Returns
    -------
    Un dico
    """

    res = dict()
    l_filieres = liste_filieres(df)

    for i in l_filieres:
        # on recupere la liste des etablissements de cette filiere
        l_c = list(df[df['fili'] == i]["voe_tot"])
        l_c_int = [int(l_c[i]) for i in range(len(l_c))]
        l_p = list(df[df['fili'] == i]["prop_tot"])
        l_p_int = [int(l_p[i]) for i in range(len(l_p))]
        l_a = list(df[df['fili'] == i]["nb_admis"])
        l_a_int = [int(l_a[i]) for i in range(len(l_a))]

        # nb_candidats représente le nombre de candidats à une filière, nb_propositions le nombre de
        # candidats qui se sont vus proposer la filière et nb_acceptations le nb de candidats qui l'ont accepté
        res[i] = {'nb_candidatures': sum(l_c_int), 'nb_propositions': sum(
            l_p_int), 'nb_acceptations': sum(l_a_int)}

    return res


def classification_par_filiere_fine(dataframe, liste_filiere):
    """
    classification_par_filiere_fine renvoie un dicitonnaire organisé par filières fines

    Parameters
    ----------
    dataframe: le dataframe sur lequel on travaille

    liste_filiere: list
            Liste de filières dont on veut extraire les filières fines
            (par exemple : liste_filiere = ['3_BTS', '4_CPGE'])

    Returns
    -------
    { filiere_fine1 : { lycée1 : {capacité : , rang_dernier_admis: , nombre_mentions_tb: , ... },

                   lycée2 : { … },

                 },

      filiere_fine2 : { lycée1 : { … } ,

                   lycée2 : { … },

                 },
    }
    """

    # Initialisation de la forme du résultat
    res = dict()

    # On crée la liste des filières fines qu'on va considérer
    filieres = []
    for i in range(len(liste_filiere)):
        filieres += liste_filieres_fines(dataframe, liste_filiere[i])
    nb_filieres = len(filieres)
    for i in range(nb_filieres):
        res[filieres[i]] = {}
    # Ici, on a res = {filiere_fine1 : {} , filiere_fine2 : {} , ...}

    # On charge toutes les colonnes du dataset dont on a besoin
    filiere_fine = dataframe['filiere_fine']
    nom_etab = dataframe['nom_etablissement']
    capacite = dataframe['capa_fin']
    nb_admis = dataframe['nb_admis']
    nb_admis_f = dataframe['nb_admis_f']
    nb_admis_voeu1 = dataframe['nb_admis_voe_1']
    nb_admis_voeu1_f = dataframe['nb_admis_voe1_f']
    nb_boursiers = dataframe['nb_boursiers']
    nb_tres_bien = dataframe['nb_tres_bien']
    nb_bien = dataframe['nb_bien']
    nb_assez_bien = dataframe['nb_assez_bien']
    nb_no_mention = dataframe['nb_no_mention']
    nb_voeu1 = dataframe['voe1']
    nb_voeu1_f = dataframe['voe1_f']

    # On remplit alors le dictionnaire résultat
    n = len(filiere_fine)
    for i in range(n):
        # Pour chaque établissement du dataframe
        if filiere_fine[i] in filieres:
            # Si l'établissement a pas encore été pris en compte pour cette filière (par exemple dans le cas où l'établissement a plusieurs sous filieres)
            if (nom_etab[i] not in res[filiere_fine[i]].keys()):
                res[filiere_fine[i]][nom_etab[i]] = {'capacite': int(capacite[i]), 'nb_admis': int(nb_admis[i]), 'nb_admis_f': int(nb_admis_f[i]), 'nb_admis_voeu1': int(nb_admis_voeu1[i]),
                                                     'nb_admis_voeu1_f': int(nb_admis_voeu1_f[i]), 'nb_boursiers': int(nb_boursiers[i]), 'nb_tres_bien': int(nb_tres_bien[i]),
                                                     'nb_bien': int(nb_bien[i]), 'nb_assez_bien': int(nb_assez_bien[i]), 'nb_no_mention': int(nb_no_mention[i]),
                                                     'nb_voeu1': int(nb_voeu1[i]), 'nb_voeu1_f': int(nb_voeu1_f[i])}

            else:  # Sinon, ie si l'établissement a déjà été pris en compte
                a = res[filiere_fine[i]][nom_etab[i]]
                a['capacite'] += int(capacite[i])
                a['nb_admis'] += int(nb_admis[i])
                a['nb_admis_f'] += int(nb_admis_f[i])
                a['nb_admis_voeu1'] += int(nb_admis_voeu1[i])
                a['nb_boursiers'] += int(nb_boursiers[i])
                a['nb_tres_bien'] += int(nb_tres_bien[i])
                a['nb_bien'] += int(nb_bien[i])
                a['nb_assez_bien'] += int(nb_assez_bien[i])
                a['nb_no_mention'] += int(nb_no_mention[i])
                a['nb_voeu1'] += int(nb_voeu1[i])
                a['nb_voeu1_f'] += int(nb_voeu1_f[i])

    return res


def moy_attractivite_dep(df, filiere):
    """ 
    moy_attractivite_dep renvoie une liste contenant les noms des différents départements ainsi que la moyenne d'attractivité 
    pour une filière, sous filière ou filière fine donnée 

    Parameters
    ----------
    df : dataframe sur lequel on travaille 

    filiere : str 
        Nom de la filière, filière fine ou sous filière pour laquelle on veut l'attractivité par région

    Returns 
    -------
    liste_ind : list 
        liste de la forme [[moyenne d'attractvité pour un département et une filière donnée, nom du département], ... ]

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

    def indice(df):
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

        # On récupère les listes des valeurs qui nous intéressent pour calculer l'indice d'attractivité : le nombre de voeux 1
        # pour cet établissement, le nombre de voeux totaux, le nombre d'admis, le pourcenatge de mentions bien et de mentions
        # très bien pour les élèves admis dans l'établissement )
        liste_rang_dernier_admis = list(df['rang_der_max'])
        liste_voeux_1 = list(df['voe1'])
        liste_nb_voeux_tot = list(df['voe_tot'])
        liste_nb_admis = list(df['nb_admis'])
        liste_p_tres_bien = list(df['p_admis_tres_bien'])
        liste_p_bien = list(df['p_admis_bien'])
        moy_indice = []
        if len(liste_nb_admis) > 0:
            for i in range(len(liste_nb_admis)):
                # Calcul de l'indice
                indice = 0.9*(int(liste_voeux_1[i])/int(liste_nb_voeux_tot[i])) - 0.1*((int(
                    liste_rang_dernier_admis[i])-int(liste_nb_admis[i]))/int(liste_nb_voeux_tot[i]))
                indice = 0.8*indice + 0.15 * \
                    liste_p_tres_bien[i] + 0.05*liste_p_bien[i]
                moy_indice.append(float(indice))
            return np.nanmean(moy_indice)
        else:
            return 0

    def change_df(df, filiere):
        if filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere':
            df_2 = df[df['fili'] == filiere]
            return df_2
        elif filiere_filiere_fine_ou_sous_filiere(filiere) == 'filiere_fine':
            df_2 = df[df['filiere_fine'] == filiere]
            return df_2
        elif filiere_filiere_fine_ou_sous_filiere(filiere) == 'sous_filiere':
            df_2 = df[df['sous_filiere'] == filiere]
            return df_2
        else:
            return df

    liste_ind = []
    df_2 = change_df(df, filiere)
    liste_dep = liste_departements(df)
    for departement in liste_dep:
        liste_ind_dep = []
        liste_etablissement = []
        df_3 = df_2[df_2['nom_dep'] == departement]
        L = list(df_3['nom_dep'])
        if len(L) > 0:
            for etablissement in df_3['nom_etablissement']:
                if etablissement not in liste_etablissement:
                    liste_etablissement.append(etablissement)
                    df_4 = df_3[df_3['nom_etablissement'] == etablissement]
                    indic = indice(df_4)
                    liste_ind_dep.append(indic)
            moy = np.nanmean(liste_ind_dep)
            liste_ind.append([moy, departement])
        else:
            liste_ind.append([0, departement])

    return liste_ind


def liste_sous_filiere2(df, filiere_fine):
    """
    liste_sous_filiere2 renvoie la liste des sous filières d'une filière fine présente sur le dataframe
    (par exemple, les filières fines de Classe préparatoire scientifique sont MPSI, PCSI, PTSI, ...

    Parameters
    ----------
    dataframe : dataframe sur lequel on travaille
    filiere_fine : str
        Nom de la filière fine dont on veut connaitre les sous filieres

    Returns
    -------
    list : [sous_filiere1, sous_filiere2, ...]
    (ou None si la filière n'existe pas)
    """

    df_fili = df[df['filiere_fine'] == filiere_fine]
    L = list(df_fili['sous_filiere'])

    if (len(L) == 0):
        return None

    else:
        L2 = [L[0]]
        for sousfili in L:
            if sousfili not in L2:
                L2.append(sousfili)
        return L2
