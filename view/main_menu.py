from utils.settings import colorise, clear_console


class MainMenu:
    def display_menu(self):
        print("Saisie des informations du Club d'échecs.\n")
        menu = input(
            colorise(
                "Quel menu souhaitez-vous sélectionner ?\nSaisir le numéro souhaité :\n\n"
                + " 1 - Gestion des joueurs,\n"
                + " 2 - Gestion des tournois,\n"
                + " 3 - Gestion des rapports,\n"
                + " 0 - Quitter.\n"
            )
        )
        clear_console()
        return menu
