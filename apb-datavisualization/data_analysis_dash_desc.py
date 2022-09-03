# Fichier de descriptions des graphes dash

def dash_desc(type_donnees):
    """
    Cette fonction renvoie la description correspondant au bon graphe.

    Parameters
    ----------
    type_donnees : chaîne de caracteres appartenant à liste_label définie dans app.py 

    Returns
    -------
    desc : chaîne de caractères correspondant à la description du graphe
    """
    if type_donnees == "Taux de filles dans les différentes filières":
        desc = "Ces histogrammes représentent la proportion de filles dans les différentes filières. \n \nIl est possible de sélectionner une filière parmi celles proposées et ainsi obtenir une visualisation plus fine. \nLes taux sont calculés par rapport à l'effectif de la filière considérée."
        return desc

    elif type_donnees == "Nombre de candidatures, de propositions et d'affectations dans les différentes filières":
        desc = "Ces histogrammes représentent le nombre de candidatures, de propositions faites par les filières aux étudiants et des affectations des étudiants. \nLes résultats étant donnés sous forme de taux ramenés à la capacité de la filière et peuvent donc être supérieurs à un lorsqu'il y a plus de candidatures que de places, ou finalement plus de places offertes que la capacité d'origine"
        return desc

    elif type_donnees == "Carte de France colorée selon l'attractivité du département pour une filière donnée":
        desc = "Cette carte représente la moyenne d'attractivité des établissements au sein d'un même département. \nLe calcul de l'indice d'attractivité prend en compte : la proportion d'étudiants l'ayant classé en premier voeu, le rang du dernier admis rapporté au nombre de candidats et les proportions de mentions TB et B"
        return desc

    elif type_donnees == "Carte de France des filières accueillant le plus d'élèves par département":
        desc = "Cette carte représente la filière accueillant le plus d'étudiants pour chaque département de France métropolitaine."
        return desc

    elif type_donnees == "Répartition du nombre de voeux de rang 1 selon les filières":
        desc = "Ce graphique représente la proportion de voeux de rang 1 selon les différentes filières."
        return desc

    elif type_donnees == "Evolution entre 2016 et 2017 de la répartition du nombre de voeux de rang 1 selon les filières":
        desc = "Ce graphique représente l'évolution de la répartition des voeux de rang 1 dans les différentes filières entre 2016 et 2017."
        return desc

    elif type_donnees == "Nombre de places disponibles dans les différentes filières":
        desc = "Ce diagramme circulaire montre la répartition des places disponibles dans les différentes filières."
        return desc

    elif type_donnees == "Nombre d'établissements proposant chaque filière":
        desc = "Ce diagramme circulaire montre la répartition des établissemennts proposant chaque filière."
        return desc

    elif type_donnees == "Evolution entre 2016 et 2017 du taux de filles dans les différentes filières":
        desc = "Cet histogramme représente l'évolution de la proportion d'étudiantes selon les filières entre 2016 et 2017. \nLes taux sont calculés par rapport à l'effectif de la filière considérée."
        return desc

    elif type_donnees == "Taux de boursiers dans les différentes filières":
        desc = "Ces histogrammes représentent la proportion de boursiers dans les différentes filières. \nIl est possible de sélectionner une filière parmi celles proposées et ainsi obtenir une visualisation plus fine. \nLes taux sont calculés par rapport à l'effectif de la filière considérée."
        return desc

    elif type_donnees == "Evolution entre 2016 et 2017 du taux de boursiers dans les différentes filières":
        desc = "Cet histogramme représente l'évolution de la proportion de boursiers selon les filières entre 2016 et 2017. \nLes taux sont calculés par rapport à l'effectif de la filière considérée."
        return desc

    elif type_donnees == "Répartition des mentions des élèves admis pour une filière donnée et un établissement donné":
        desc = "Ce diagramme circulaire donne la répartion des mentions obtenues au baccalauréat par les élèves admis dans un établissement et une filière donnée. \nIl est possible de choisir la filière et l'établissement en les sélectionnant ci-dessous."
        return desc

    elif type_donnees == "Etablissements les plus attractifs au sein d'une filière":
        desc = "Ce graphique donne le classement des établissements les plus attractifs pour chaque filière. \nIl est possible de choisir le nombre d'établissements apparaissant dans le classement  \nLe calcul de l'indice d'attractivité prend en compte : la proportion d'étudiants l'ayant classé en premier voeu, le rang du dernier admis rapporté au nombre de candidats et les proportions de mentions TB et B.\nIl est ensuite ramené sur [0,1] pour le nombre d'établissements considéré"
        return desc

    elif type_donnees == "Filières les plus attractives au sein d'un même établissement":
        desc = "Ce graphique représente les filières les plus attractives au sein d'un même établissement que l'on peut sélectionner ci-dessous. \nLe calcul de l'indice d'attractivité prend en compte : la proportion d'étudiants l'ayant classé en premier voeu, le rang du dernier admis rapporté au nombre de candidats et les proportions de mentions TB et B."
        return desc

    elif type_donnees == "Proportion d'étudiants allant dans une filière mais dans un voeu n'était pas leur premier choix":
        desc = "Ce graphique représente la proportion d'étudiants allant dans une filière mais dont le premier choix ne leur a pas été accordé."
        return desc

    elif type_donnees == "Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée":
        desc = "Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée"

    elif type_donnees == "Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée":
        desc = "Classement des établissements selon la proportion d'admis avec mention très bien pour une filière donnée"
