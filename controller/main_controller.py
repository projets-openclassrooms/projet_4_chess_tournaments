import os
from controller.control_players import PlayerManager
from controller.control_reports import ReportManager
from controller.control_tournaments import TournamentManager
from view.main_menu import MainMenu

from CONSTANTES import DATA_FOLDER, clear

""""
import random pour 1er round
ensuite en fonction du scoring



"""


class MainController:
    def __init__(self):
        self.tournament = TournamentManager()
        self.player = PlayerManager()
        self.report = ReportManager()
        self.mainview = MainMenu()

    def run(self):
        if not os.path.exists(DATA_FOLDER):
            os.mkdir(DATA_FOLDER)
        # creer un fichier vierge json pour les players
        if not os.path.exists(os.path.join(DATA_FOLDER, "players.json")):
            with open(os.path.join(DATA_FOLDER, "players.json"), "w") as f:
                f.write("{}")
        # creer un fichier vierge json pour les tournois
        if not os.path.exists(os.path.join(DATA_FOLDER, "tournaments.json")):
            with open(os.path.join(DATA_FOLDER, "tournaments.json"), "w") as f:
                f.write("{}")

        menu = ""
        while menu != "0":
            menu = self.mainview.display_menu()
            if menu == "1":
                clear()
                self.player.run_player()
            elif menu == "2":
                self.tournament.run_tournament()
            elif menu == "3":
                self.report.run_report()
            elif menu == "0":
                break
            else:
                print("Réponse (1/2/3/0) svp.")
