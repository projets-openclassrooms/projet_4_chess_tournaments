from utils.settings import colorise


class MainMenu:
    def display_menu(self):
        menu = input(colorise(
            "Quel menu souhaitez-vous sélectionner ?\nTaper le numéro souhaité :\n\n"
            + " 1 - Gestion des joueurs,\n"
            + " 2 - Gestion des tournois,\n"
            + " 3 - Gestion des rapports,\n"
            + " 0 - Quitter.\n")
        )
        return menu
