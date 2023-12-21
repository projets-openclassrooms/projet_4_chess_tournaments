

class MainMenu:
    def display_menu(self):
        menu = input(
            "Quel menu souhaitez-vous sélectionner ?\nTaper\n\n"
            + " 1 - Créer un nouveau joueur \n"
            + " 2 - Gestion du tournoi\n"
            + " 3 - Gestion des rapports\n"
            + " 4 - Supprimer un joueur\n"
            + " 5 - Modifier un joueur\n"
            + " 6 - Voir les joueurs\n"
            + " 7 - Créer un nouveau tournoi\n"
            + " 8 - Voir les tournois\n"
            + " 0 - quitter.\n"
        )
        return menu

