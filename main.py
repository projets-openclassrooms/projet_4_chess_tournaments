# encoding: utf-8
from CONSTANTES import TOURNAMENT_FOLDER
from controller.main_controller import MainController

# DATA_FOLDER = "data/"


if __name__ == "__main__":
    # TODO couleur ecran
    maincontroller = MainController()
    maincontroller.run()

# dict pour retourner objet
# list to dict pour json
# dict to list pour afficher, modifier
# 1 - Gestion joueur
# # Quel menu souhaitez-vous selectionner ?
# # Taper

# #  1 - Cr?er un nouveau joueur
# #  2 - Supprimer un joueur #bug pas obligatoire
# #  3 - Modifier un joueur # liste puis bug sur cle, valeur lues pas obligatoire
# #  4- Voir les joueurs
# #  0 - quitter.

# 2 - Gestion du tournoi
# # (1) Voulez-vous creer un nouveau tournoi, #bug pas 1st turn
# message
# Quel est le nom de ce tournoi? ('0' pour revenir au menu)
# Ou se passe ce tournoi? (tapez '0' pour revenir au menu)
# Votre liste de joueurs s?lectionn?s est vide.
# Les joueurs deja enregistres sont:
# 1-Le joueur DRE - INE , DD11111 (score: 0)
# 2-Le joueur PASTEUR - INE , LP00010 (score: 0)
# 3-Le joueur DIA - INE , SD12456 (score: 0)
# 4-Le joueur FER - INE , FF12345 (score: 0)

# Choix des joueurs : taper l'identification du joueur ou  utiliser les options suivantes :
#  -Taper 1 pour afficher la liste en cours d'entree.
#  -Taper 2 pour selectionner tous les joueurs.
#  -Taper '0' pour quitter la creation.
# # (2) reprendre un tournoi en cours #bug
# ToDO LISTEN TOURNAMENTS puis lister avec numero
# # Saisir 1/ 2/ ou '0' pour quitter?

# 3 - Gestion des rapports
# # Quel type de rapport aimeriez-vous creer?
# # - (1) Tous les joueurs. #bug
# # - (2) Tous les tournois. #bug
# # - (3) Tous les resultats de matchs de tournoi(s). #bug
# # - (4) Tous les joueurs participant au(x) tournoi(s). #bug
# # -Ou (5) pour revenir en arriere.

# 0 - quitter.
