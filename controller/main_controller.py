import os

from model.tournament import Tournament
from controller.control_players import PlayerManager
from controller.control_reports import ReportManager
from controller.control_tournaments import TournamentManager
from view.main_menu import MainMenu
from view.playerview import PlayerView
from view.tournamentview import TournamentView

from CONSTANTES import DATA_FOLDER

""""
import random pour 1er round
ensuite en fonction du scoring



"""


class MainController:
    def __init__(self):
        self.mainview = MainMenu()
        self.tournament_view = TournamentView()
        self.tournament = TournamentManager()
        self.player = PlayerManager()
        self.report = ReportManager()

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
                # menu joueur
                
                self.player.run_player()
            elif menu == "2":
                # Gestion du tournoi
                self.tournament_view.ask_to_continue()
                self.tournament.run_tournament()
            elif menu == "3":
                # Créer un rapport sur les joueurs (format csv)
                # Créer un rapport sur les tournois  (format csv)
                self.report.run_report()
            elif menu == "0":
                break
            else:
                print("Recommencez svp.")
