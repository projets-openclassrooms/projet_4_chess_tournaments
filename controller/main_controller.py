import os

from controller.control_players import PlayerManager
from controller.control_reports import ReportManager
from controller.control_tournaments import TournamentManager
from view.main_menu import MainMenu

from CONSTANTES import DATA_FOLDER

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
        print(DATA_FOLDER)


        menu = ""
        while menu != "0":
            menu = self.mainview.display_menu()
            if menu == "1":
                self.player.run_player()
            elif menu == "2":
                self.tournament.run_tournament()
            elif menu == "3":
                self.report.run_report()
            elif menu == "0":
                break
            else:
                print("Réponse (1/2/3/0) svp.")
