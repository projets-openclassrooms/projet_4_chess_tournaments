class MainMenu:
    def display_menu(self):
        menu = input(
            "Quel menu souhaitez-vous sélectionner ?\nTaper\n\n"
            + " 1 - Gestion joueur \n"
            + " 2 - Gestion du tournoi\n"
            + " 3 - Gestion des rapports\n"
            + " 0 - quitter.\n"
        )
        return menu
    

