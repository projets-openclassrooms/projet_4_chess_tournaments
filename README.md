# projet_4_chess_tournaments OpenClassrooms

Il fonctionne en installant python (version utilisée 3.10) et en exécutant quelques commandes. Le but de l'application est la suivante:

L'application hors ligne contient une base de données des joueurs avec des fichiers JSON.

Le programme permet d'ajouter des joueurs avec des données telles que le nom, le prénom, la date de naissance et l'identifiant national d'échecs (INE).

Les tournois sont organisés en tours avec des matchs, où les joueurs reçoivent des points en fonction de leurs résultats.
1 pour le gagnant, 0.5 quand il y a égalité et 0 pour le pour le perdant.

Chaque tournoi contient des informations telles que le nom, le lieu, les dates, le nombre de tours, les joueurs enregistrés et les remarques du directeur du tournoi.

Les matchs sont générés en fonction des résultats des joueurs, en évitant les matchs identiques.

Le programme permet également de générer des rapports sur les joueurs, les tournois et les matchs, et de sauvegarder et charger les données à partir de fichiers JSON.

Le rapport sera extrait au format .csv pour pouvoir être ouvert avec un tableur comme excel.

## Installations des prérequis sous windows
Dernière version de Python https://www.python.org/download/

Pour les tests , utilisation de l'IDE Pycharm.

Placez vous dans le dossier de votre choix, puis faites :

git clone https://github.com/projets-openclassrooms/projet_4_chess_tournaments.git


## Création de l'environnement virtuel en vue d'installer les librairies
Placez vous dans le dossier cloné, puis créez un nouvel environnement virtuel:

python3 -m venv env

Activez votre environnement virtuel env nouvellement créé 
Sous Windows :

env\scripts\activate.bat

sous linux :

source env/bin/activate

## Installation librairies 
pip install -r requirements.txt

## Utilisation de l'application
Vous pouvez enfin lancer le script:
python main.py présent à la source du dossier de travail.

## Résultat
Enjoy it.
