players_data = "data/players.json"
tournaments_data = "data/tournaments.json"
MAX_PLAYERS = 8


class MainMenu:
    def display_menu(self):
        menu = input(
            "Quel menu souhaitez-vous sélectionner ?\n"
            + "Taper 1 pour Gestion des joueurs\n"
            + "Taper 2 pour Gestion du tournoi\n"
            + "Taper 3 pour Gestion des rapports\n"
            + "Ou taper 'q' pour quitter.\n"
        ).upper()
        return menu
