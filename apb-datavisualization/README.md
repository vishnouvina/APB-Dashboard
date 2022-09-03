# APB-datavisualization

Ce programme permet de visualiser différentes statistiques effectuées sur les données APB de 2016 et de 2017 grâce à une interface graphique Dash.

**POUR EXECUTER LE PROGRAMME**

Pour exécuter le programme, il faut lancer le fichier app.py

**Instructions pour installer les packages nécessaires**

Installer les modules nécessaires en tapant dans le terminal la commande suivante :  pip install -r requirements.txt

**Instructions pour exécuter le code :**

Nous avons d'abord fait une version en invite de commande accessible sur le fichier dataviz_main_command_line.py

Pour éxécuter le porgramme avec ce fichier il faut tout d'abord taper :
python dataviz_main_command_line.py "type_personne" "type_filiere" "année" "critere" "etablissement" "categorie"
dans le terminal pour voir un graphique s'afficher

Les valeurs possibles pour les différentes variables sont : 

- type_personne : 'eleve' si vous êtes un élève qui recherche des statistiues sur les années précédentes d'apb, que ce soit pour le nombre 
                de places disponibles dans tellle ou telle formation, l'attractvité des établissements en fonction du secteur qui vous intéresse
                
                'etablissement' si vous êtes un personne d'une administration d'un établissement qui sera donc plus intéressée par la répartition des boursiers ou des filles parmi les différentes filières

- type_filiere : 'filiere' si vous souahitez visualiser des statistiques sur les différentes filières 
                 
                 'filiere fine' si vous souhaitez visualiser des statistiques sur les filières fines 
                 
                 'sous filiere' si vous souhaitez visualiser des statistiques sur les sous filières

- année : '2016' pour sélectionner les données de l'année 2016
          
          '2017' pour sélectionner celles de 2017

          'les deux' si vous souhaitez comparer les statistiques des deux années

- critere : 'fille' pour visionner des statistiques ne prenant en compte que les filles 

            'boursier' pour visionner celles concernant les boursiers 

            'non' si vous ne souhaitez pas filtrer les données selon un de ces deux critères

- etablissement : soit l'orthographe précise d'un établissement présant dans la base de donnée 

                  'non' si vous ne souhaitez pas des données pour un établissement en particulier 

- categorie : 'attractivite' pour mesurer l'attractivité d'une filière ou les établissements les plus attractifs par filière 

              'frustration' pour voir le nombre de personne qui n'ont pas eu ce qu'elles voulaient en premier

              'mention' si on veut filtrer les données par mention au bac

              'proportion etablissement' si on veut déterminer la proportion d'établissement pour un critère donné

              'places' pour voir le nombre de places disponibles par filière suivant d'autres conditions 

              'demandes' pour voir le nombre de demandes 

              'refus' pour mesurer le nombre de personnes refusées dans une certaine filière, sous filière ou filière fine

Attention, certaines combinaisons de ces variables sont susceptibles de ne pas marcher du fait de notre nombre limité de graphiques

Quelques exemples de combinaisons qui fonctionnent : 

        - python dataviz_main_command_line.py "élève" "filière" "2016" "non" "non" "attractivite" renverra un nuage de point avec les établissements les plus attractifs suivant une filière, filière fine ou sous filière pour les données de 2016

        - python dataviz_main_command_line.py "élève" "filière fine" "2017" "non" "non" "refus" renverra un histogramme montrant le nombre de demandes, de propositions et d'acceptations pour une liste de filière fine et pour les données de 2017

        - python dataviz_main_command_line.py "etablissement" "sous filière" "les deux" "fille" "non" "taux" renverra un histogramme avec l'évolution sur les 2 ans de la proportion de filles dans les sous filières voulues 

Mais par exemple, python dataviz_main_command_line.py "etablissement" "filière" "2017" "non" "non" "attractivite" renverra : "Nous n'avons pas ce type de graphe" car cet enchainement de variables n'existe pas 


Nous avons ensuite choisi de passer sur dash pour une visualisation plus interactive des données, voici comment accéder à l'interface

Il faut exécuter le fichier app.py, puis se rendre à l'adresse suivante : http://127.0.0.1:8050/  

Après, l'utilisateur peut naviguer entre les différents graphiques possibles grâce à un menu déroulant.
Certains graphiques possèdent des options pouvant prendre différentes formes (cases à cocher, années à sélectionner).  


**INSTRUCTIONS POUR COMPRENDRE LE CODE :**

En ce qui concerne le code, les fichiers python s'articulent de la manière suivante :

- le fichier data_utils.py récupère les données et les nettoie en supprimant des lignes où les données sont manquantes pour rendre les données exploitables. Il sert principalement à créer un dataframe qui reprend le fichier excel et en renommant certaines colonnes.

- le fichier data_statistics.py utilise alors ce dataframe et permet d'effectuer un premier traitement pour récupérer certaines données qui seront réutiliséess dans les autres fonctions (par exemple, la liste des filières, la liste des régions, ou la liste des départements), et pour réarranger les données sous forme de dictionnaire (plus facilement exploitables).

- le fichier data_analysis.py utilise alors les fonctions de data_statistics.py afin de créer des fonctions permettant de créer différents graphiques (histogrammes, camemberts) permettant de visualiser les données, et ce grâce au module matplotlib  (dans la première version de notre code, on ne pensait pas utiliser dash).

- le fichier data_analysis_dash.py reprend les mêmes fonctions que data_analysis, mais au lieu de renvoyer un graphique issu de matplotlib, elles renvoient des figures issues de dash, afin de les afficher par la suite dans une interface graphique de Dash

- le fichier dataviz_main_command_line.py permet d'afficher les graphiques grâce à des commandes directement dans le terminal (correspond à une version de secours si Dash ne fonctionnait pas).

- le fichier data app.py exécute alors le programme et permet d'ouvrir l'interface graphique Dash

- le fichier data_analysis_dash_desc.py contient les descriptions des graphiques.

**Fichiers annexes**

- le dossier Data contient le dataframe sous le format .csv, qui est disponible [ici](https://www.data.gouv.fr/fr/datasets/apb-voeux-de-poursuite-detude-et-admissions/)

- Le document PDF décrivant notre travail préliminaire d’analyse, de conception et de découpage ainsi que l'avancée de notre projet tout au long de son élaboration.

- Le fichier disponible [ici](https://france-geojson.gregoiredavid.fr/repo/departements.geojson) que l'on récupère directement en ligne pour afficher les cartes délimitées par départements. ​

**AUTEURS**

- Evan Ichir

- Vishnou Vinayagame

- Aurélien Du Mur​

- Yanis Adel

- Grégoire Gissot

- Gauthier Arnoux De Maison Rouge




