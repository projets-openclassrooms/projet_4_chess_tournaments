"""Define report manager
export csv, txt, or html"""
import csv
import os

from CONSTANTES import REPORT_FILE, STATUS_ALL
from controller.control_players import PlayerManager
from controller.control_tournaments import TournamentManager
from model.player import Player
from model.tournament import Tournament
from view.reportview import ReportView


# REPORT_FILE = "data/report/"


class ReportManager():
# class ReportManager(Tournament):
    def __init__(self):
        # super().__init__()
        self.player = PlayerManager()
        self.report_view = ReportView()
        self.report_tournaments = TournamentManager()
        self.tournaments = Tournament()

    def all_tournaments_by_name(self):
        """

        :rtype: object
        :return all_tournaments
        """
        # self.report_tournaments.list_tournament()
        tournament_index = []
        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)
        for i, tournoi in enumerate(tournaments_data, start=1):
            print(f"Tournoi {i} : {tournoi.name} \n")
            print(f"Dates: du {tournoi.starting_date.strftime('%d/%m/Y %H:%M')} au {tournoi.ending_date}\n") #.strftime('%d/%m/Y %H:%M')
            tournament_index.append(tournaments_data[i-1])
        return tournament_index

    def report_control(self):
        """

        :rtype: object
        :return boolean
        """
        tournaments = self.tournaments.loads_tournament(status=STATUS_ALL)

        # with open(file, "w"):
        for i, tournament in enumerate(tournaments):
            print(f"{i + 1}. {tournament.name}")

        while True:
            try:
                choice = int(input("\nSélectionnez un tournoi par son numéro : "))
                if 1 <= choice <= len(tournaments):
                    return tournaments[choice - 1]
                else:
                    print("Veuillez choisir un numéro valide.")
            except ValueError:
                print("Veuillez choisir un numéro valide.")

        self.report_view.display_create_report()

    def open_selected_report(self, tournament_index):
        """
        open files to open

        :rtype: object

        """
        tournament_name = int(input("Entrer numéro du tournoi à afficher : "))
        if tournament_name == tournament_index:
            print(tournament_index)

    def save_players_report(self):
        """Export a list of all players saved"""

        all_players = Player.get_players_saved()

        title = ["Nom", "Prénom", "Date de Naissance", "identifiant"]
        data = []
        for player in all_players:
            player_extract = [
                player.name,
                player.firstname,
                player.date_of_birth,
                player.national_identification,
            ]
            data.append(player_extract)
        file_name = REPORT_FILE + "all_players_saved.csv"

        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(title)
            writer.writerows(data)
        self.open_selected_report()
        self.report_view.display_create_report()

    def all_players_tournament_report(self):
        """Export a list of players from a selected tournament
        in alphabetic order"""
        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)
        for i, tournoi in enumerate(tournaments_data, start=1):
            players_by_id = tournoi.players
            print ({i} - {tournoi.name} - {tournoi.description} - {tournoi.ending_date})
            sorted_players = sorted(players_by_id, key=lambda classe: (classe.name, classe.firstname))
            for player in sorted_players:
                print(player.name, player.firstname)

    def run_report(self):
        """ liste des joueurs par ordre alphabétique ;
            liste des tournois ;
            Nom et dates d’un tournoi donné ;
            liste des joueurs du tournoi par ordre alphabétique ;
            liste de tous les tours du tournoi et de tous les matchs du tour.
         """

        while True:
            selection = self.report_view.get_type_report()

            if selection == 1:
                self.player.display_players()
                self.save_players_report()
            elif selection == 2:
                self.report_tournaments.list_tournament()
            elif selection == 3:
                self.all_tournaments_by_name()
            elif selection == 4:
                self.all_players_tournament_report()
            elif selection == 5:
                self.report_control()
            else:
                selection == 6
                break
