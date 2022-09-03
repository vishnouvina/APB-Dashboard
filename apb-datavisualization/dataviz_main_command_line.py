from data_analysis_dash import *
from data_statistics import *
from data_utils import *
import unicodedata
import string

import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "type_personne", help="type de personne qui veut visualiser des données : établissement ou élève")
parser.add_argument(
    "type_categorie", help="visualiser filière, filière fine ou sous filière")
parser.add_argument("year", help="année demandée : 2016, 2017 ou les deux")
parser.add_argument("critere", help='critère voulu')
parser.add_argument(
    "etablissement", help="stats sur un établissment particulier ou non")
parser.add_argument(
    "categorie", help="à quelle donnée s'intéresse-t-on en particulier")
args = parser.parse_args()


def main():
    df2016 = load_dataframe(2016)
    df2017 = load_dataframe(2017)
    type_personne = args.type_personne
    type_cat = args.type_categorie
    year = args.year
    critere = args.critere
    etablissement = args.etablissement
    cat = args.categorie
    if year == '2016' or year == '2017':
        year = int(year)
    if type_personne == 'eleve':
        if critere == 'non':
            if cat == 'refus':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if year == 2016:
                            fig = dash_histogramme_refus_filiere(df2016)
                            fig.show()
                        else:
                            fig = dash_histogramme_refus_filiere(df2017)
                            fig.show()
                    elif type_cat == 'filiere fine':
                        l_filieres = list(
                            input('Entrer la liste des filières fines : :'))
                        if year == 2016:
                            fig = dash_histogramme_refus_filere_fine(
                                df2016, l_filieres)
                            fig.show()
                        else:
                            fig = dash_histogramme_refus_filere_fine(
                                df2017, l_filieres)
                            fig.show()
                    else:
                        l_filieres = list(
                            input('Entrer la liste des sous filières : '))
                        if year == 2016:
                            fig = dash_histogramme_refus_sous_filiere(
                                df2016, l_filieres)
                            fig.show()
                        else:
                            fig = dash_histogramme_refus_sous_filiere(
                                df2017, l_filieres)
                            fig.show()
                else:
                    print("Nous n'avons pas actuellement ce type de graphe")
            elif cat == 'demandes':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            fig = dash_histo_plus_demande_annees(
                                df2016, df2017)
                            fig.show()
                        else:
                            if year == 2016:
                                fig = dash_histo_plus_demande(df2016)
                                fig.show()
                            else:
                                fig = dash_histo_plus_demande(df2017)
                                fig.show()
                    else:
                        print("Nous n'avons pas actuellement ce type de graphe")
                else:
                    print("Nous n'avons pas actuellement ce type de graphe")
            elif cat == 'places':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            if year == 2016:
                                fig = dash_camembert_filieres_places_disponibles(
                                    df2016)
                                fig.show()
                            else:
                                fig = dash_camembert_filieres_places_disponibles(
                                    df2017)
                                fig.show()
                    else:
                        print("Nous n'avons pas actuellement ce type de graphe")
                else:
                    print("Nous n'avons pas actuellement ce type de graphe")

            elif cat == 'proportion etablissement':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            if year == 2016:
                                fig = dash_camembert_proportion_etablissement_filieres(
                                    df2016)
                                fig.show()
                            else:
                                fig = dash_camembert_proportion_etablissement_filieres(
                                    df2017)
                                fig.show()
                    else:
                        print("Nous n'avons pas actuellement ce type de graphe")
                else:
                    print("Nous n'avons pas actuellement ce type de graphe")
            elif cat == 'mention':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            l_filieres = list(
                                input("Entrer la liste des filières que vous voulez : "))
                            if year == 2016:
                                fig = dash_histogramme_excellence_academique(
                                    df2016, l_filieres, n)
                                fig.show()
                            else:
                                fig = dash_histogramme_excellence_academique(
                                    df2017, l_filieres, n)
                                fig.show()
                    else:
                        print("Nous n'avons pas actuellement ce type de graphe")
                else:
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            etablissement = input(
                                "Entrer le nom de l'établissement désiré (attention à l'orthographe) : ")
                            l_filieres = list(
                                input("Entrer la liste des filières que vous voulez : "))
                            if year == 2016:
                                fig = dash_camembert_mention_par_etablissement_par_filiere2(
                                    df2016, etablissement, l_filieres)
                                fig.show()
                            else:
                                fig = dash_camembert_mention_par_etablissement_par_filiere2(
                                    df2017, etablissement, l_filieres)
                                fig.show()
                    else:
                        print("Nous n'avons pas actuellement ce type de graphe")
            elif cat == 'frustration':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            if year == 2016:
                                fig = dash_histogramme_frustration_filieres(
                                    df2016)
                                fig.show()
                            else:
                                fig = dash_histogramme_frustration_filieres(
                                    df2017)
                                fig.show()
                    else:
                        print("Nous n'avons pas actuellement ce type de graphe")
                else:
                    print("Nous n'avons pas actuellement ce type de graphe")

            elif cat == 'attractivite':
                if etablissement == 'non':
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            filiere = input(
                                "Entrer le nom de la filière désirée : ")
                            if year == 2016:
                                fig = dash_viz_attractivite(filiere, df2016, n)
                                fig.show()
                            else:
                                fig = dash_viz_attractivite(filiere, df2017, n)
                                fig.show()

                    elif type_cat == 'filiere fine':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            filiere = input(
                                "Entrer le nom de la filière fine : ")
                            if year == 2016:
                                fig = dash_viz_attractivite(filiere, df2016, n)
                                fig.show()
                            else:
                                fig = dash_viz_attractivite(filiere, df2017, n)
                                fig.show()

                    elif type_cat == 'sous filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            filiere = input(
                                "Entrer le nom de la sous filière : ")
                            if year == 2016:
                                fig = dash_viz_attractivite(filiere, df2016, n)
                                fig.show()
                            else:
                                fig = dash_viz_attractivite(filiere, df2017, n)
                                fig.show()

                else:
                    if type_cat == 'filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            type_cat = 'filiere'
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            etablissement = input(
                                "Entrer le nom de l'établissement désiré (attention à l'orthographe) : ")
                            if year == 2016:
                                fig = dash_attractivite_etablissement(
                                    etablissement, df2016, n, type_cat)
                                fig.show()
                            else:
                                fig = dash_attractivite_etablissement(
                                    etablissement, df2017, n, type_cat)
                                fig.show()
                    elif type_cat == 'filiere fine':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            type_cat = 'filiere_fine'
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            etablissement = input(
                                "Entrer le nom de l'établissement désiré (attention à l'orthographe) : ")
                            if year == 2016:
                                fig = dash_attractivite_etablissement(
                                    etablissement, df2016, n, type_cat)
                                fig.show()
                            else:
                                fig = dash_attractivite_etablissement(
                                    etablissement, df2017, n, type_cat)
                                fig.show()

                    elif type_cat == 'sous filiere':
                        if not isinstance(year, (int, float)):
                            print("Nous n'avons pas actuellement ce type de graphe")
                        else:
                            type_cat = 'sous_filiere'
                            n = int(
                                input("Entrer le nombre d'établissements que vous voulez observer : "))
                            etablissement = input(
                                "Entrer le nom de l'établissement désiré (attention à l'orthographe) : ")
                            if year == 2016:
                                fig = dash_attractivite_etablissement(
                                    etablissement, df2016, n, type_cat)
                                fig.show()
                            else:
                                fig = dash_attractivite_etablissement(
                                    etablissement, df2017, n, type_cat)
                                fig.show()

            else:
                print("Nous n'avons pas actuellement ce type de graphe")
        else:
            print("Nous n'avons pas actuellement ce type de graphe")

    elif type_personne == 'etablissement':
        if cat != "taux" or etablissement != "non":
            print("Nous n'avons pas ce type de graphe")
        else:
            if type_cat == 'filiere':
                if not isinstance(year, (int, float)):
                    fig = dash_evolution_histogramme_taux_critere_par_filiere(
                        df2016, df2017, critere)
                    fig.show()
                else:
                    if year == 2016:
                        fig = dash_histogramme_taux_critere_par_filiere(
                            df2016, critere)
                        fig.show()
                    else:
                        fig = dash_histogramme_taux_critere_par_filiere(
                            df2017, critere)
                        fig.show()
            elif type_cat == 'filiere fine':
                liste_filiere_fine = list(input(
                    "Entrer la liste des filières fines : "))
                if not isinstance(year, (int, float)):
                    fig = dash_evolution_histogramme_taux_critere_par_filiere_fine(
                        df2016, df2017, liste_filiere_fine, critere)
                    fig.show()
                else:
                    if year == 2016:
                        fig = dash_histogramme_taux_critere_par_filiere_fine(
                            df2016, liste_filiere_fine, critere)
                        fig.show()
                    else:
                        fig = dash_histogramme_taux_critere_par_filiere_fine(
                            df2017, liste_filiere_fine, critere)
                        fig.show()
            elif type_cat == 'sous filiere':
                liste_sous_filiere = list(
                    input("Entrer la liste des sous filières : "))
                if not isinstance(year, (int, float)):
                    fig = dash_evolution_histogramme_taux_critere_par_sous_filiere(
                        df2016, df2017, liste_sous_filiere, critere)
                    fig.show()
                else:
                    if year == 2016:
                        fig = dash_histogramme_taux_critere_par_sous_filiere(
                            df2016, liste_sous_filiere, critere)
                        fig.show()
                    else:
                        fig = dash_histogramme_taux_critere_par_sous_filiere(
                            df2017, liste_sous_filiere, critere)
                        fig.show()

    else:
        print("Nous ne founissons pas de statistiques pour ce type de personne")


if __name__ == '__main__':
    main()
