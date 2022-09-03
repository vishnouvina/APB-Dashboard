"""chargement et traitement au prélable du jeu de données 
"""

# import des modules
import pandas as pd
import numpy as np

# Après le renommage le nom des colonnes est : { session, cod_uai, nom_etablissement, num_dep, nom_dep, acad_mies,
# nom_reg, fili, filiere_fine, sous_filiere, capa_fin, rang_der_max, voe_tot, voe_tot_f, voe1, voe1_f, prop_tot,
# prop_tot_f, nb_admis, nb_admis_f, nb_admis_voe1, nb_admis_voe1_f, nb_boursiers, nb_no_mention, nb_assez_bien,
# nb_bien, nb_tres_bien, nb_lycee_origine, nb_lycee_origine_f, nb_acad_origine, p_admis_acad_origine, p_admis_lycee_origine
# p_admis_boursier, p_admis_no_mention, p_admis_assez_bien, p_admis_bien, p_admis_tres_bien }


def load_dataframe(year):

    # chargement du dataframe principal

    df = pd.read_csv('./Data/fr-esr-apb_voeux-et-admissions.csv', sep=';')

    # renommer les colonnes
    df.rename(columns={'g_ea_lib_vx': 'nom_etablissement',    # nom de l'etablissement
                       'dep': 'num_dep',                         # numero du département
                       'lib_dep': 'nom_dep',                     # nom du departement
                       'lib_reg': 'nom_reg',                     # nom de la region
                       # filiere fine, filière générale (par ex: Classe prépa )
                       'form_lib_voe_acc': 'filiere_fine',
                       # sous_filiere (ex : MPSi)
                       'fil_lib_voe_acc': 'sous_filiere',
                       'acc_tot': 'nb_admis',
                       'acc_tot_f': 'nb_admis_f',
                       'acc_voe1': 'nb_admis_voe_1',
                       'acc_voe1_f': 'nb_admis_voe1_f',
                       'acc_boursier': 'nb_boursiers',
                       'acc_passable': 'nb_no_mention',
                       'acc_assez_bien': 'nb_assez_bien',
                       'acc_bien': 'nb_bien',
                       'acc_tres_bien': 'nb_tres_bien',
                       'acc_term': 'nb_lycee_origine',
                       'acc_academies': 'nb_acad_origine',
                       'p_acc_term': 'p_admis_lycee_origine',
                       'p_acc_academies': 'p_admis_acad_origine',
                       'p_acc_boursier': 'p_admis_boursier',
                       'p_acc_passable': 'p_admis_no_mention',
                       'p_acc_assez_bien': 'p_admis_assez_bien',
                       'p_acc_bien': 'p_admis_bien',
                       'p_acc_tres_bien': 'p_admis_tres_bien'}, inplace=True)

    # supprime les lignes qui contiennent 'inconnu' dans la colonne 'capa_fin' ou 'rang_dr_max'

    def sup_lign_inconnu(df):
        set_index = set([])
        for idx, column in enumerate(df.columns):
            set_index = set_index | set(
                df[df[column] == 'inconnu'].index.tolist())
            set_index = set_index | set(df[df[column] == 'ns'].index.tolist())
        list_index = list(set_index)
        df.drop(list_index, 0, inplace=True)

    sup_lign_inconnu(df)

    # separation du df en deux (année 2016 et année 2017) et réindexation
    df_2016 = df[df['session'] == 2016]
    df_2017 = df[df['session'] == 2017]

    # on enlève la colonne 'session' qui ne sert plus à rien
    df_2016.drop(["session"], axis='columns', inplace=True)
    df_2017.drop(["session"], axis='columns', inplace=True)
    if year == 2016:
        return df_2016.reset_index(drop=True)  # on réindexe le dataframe
    else:
        return df_2017.reset_index(drop=True)  # on réindexe le dataframe
