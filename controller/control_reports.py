"""Define report manager
export csv, txt, or html"""
import csv
import os

from model.match import Match
from model.player import Player
from model.turn import Turn
from model.tournament import Tournament
from view.reportview import ReportView
from CONSTANTES import REPORT_FILE


# REPORT_FILE = "data/report/"


class ReportManager:
    def __init__(self):
        self.reportview = ReportView()

    def all_tournaments_name(self):
        """

        :rtype: object
        :return all_tournaments
        """
        all_tournaments = Tournament.get_all_tournament_names()
        if all_tournaments == []:
            self.reportview.display_empty()
            return None
        return all_tournaments

    def report_control(self, file):
        """

        :rtype: object
        :return boolean
        """
        tournaments = self.all_tournaments_name()
        open_verif = None
        if open_verif:
            # with open(file, "w"):
            for i, tournament in enumerate(tournaments):
                print(f"{i + 1}. {tournament['name_of_tournament']}")

            while True:
                try:
                    choice = int(input("\nSélectionnez un tournoi par son numéro : "))
                    if 1 <= choice <= len(tournaments):
                        return tournaments[choice - 1]
                    else:
                        print("Veuillez choisir un numéro valide.")
                except ValueError:
                    print("Veuillez choisir un numéro valide.")
            else:
                open_verif = True
        path_control = os.path.exists(file)
        if path_control and open_verif:
            self.reportview.display_create_report()
            return True
        else:
            self.reportview.display_create_error()
            return False







    def open_selected_report(self, file_to_open):
        """
        open files to open

        :rtype: object

        """
        pass

    def all_tournaments_report(self):
        """Export a list of all tournaments
        :return: reports
        """
        extraction = []
        all_tournaments = self.all_tournaments_name()
        if not all_tournaments:
            return None
        title = [
            "Nom",
            "Place",
            "Joueurs inscrits",
            "date début",
            "date fin",
            "Commentaires",
        ]

        for tournament in all_tournaments:
            current = Tournament.get_tournament_info(tournament)
            if current is None:
                break
            extraction.append(
                [
                    current.name,
                    current.location,
                    current.players,
                    current.starting_date,
                    current.ending_date,
                    current.comment,
                ]
            )
        file_name = REPORT_FILE + "all_tournaments.csv"
        verification = self.report_control(file_name)
        if verification:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(title)
                writer.writerows(extraction)
            self.open_selected_report(file_name)
        else:
            # add a message if verification fails.
            self.reportview.display_create_error()



    def all_players_report(self):
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
        verification = self.report_control(file_name)
        if verification:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(title)
                writer.writerows(data)
            self.open_selected_report(file_name)
        else:
            # add a message if verification fails.
            self.reportview.display_create_error()

    def all_players_tournament_report(self):
        """Export a list of players from a selected tournament
        in alphabetic order"""
        tournament = self.get_chosen_tournament()
        if not tournament:
            return None
        title = [
            "Nom du Tournoi",
            "Joueurs - INE",
        ]
        all_tournament_player = []
        for player_identity in tournament.players:
            player_restored = Player.get_serialized_player(player_identity)
            all_tournament_player.append(player_restored.name)
        sorted_player = sorted(all_tournament_player, reverse=True)
        file_name = f"{REPORT_FILE}/{tournament.name}_all_players.csv"
        file_name = file_name.replace(" ", "")
        verification = self.report_control(file_name)
        if verification:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(title)
                for player_name in sorted_player:
                    writer.writerow([tournament.name] + [player_name])
            self.open_selected_report(file_name)

    def run_report(self):
        end_execution = False
        while end_execution is False:
            selection = self.reportview.ask_type_report()
            if selection == 5:
                end_execution = True
                break
            elif selection == 1:
                self.all_players_report()
            elif selection == 2:
                self.all_tournaments_report()
            elif selection == 3:
                self.all_matches_and_turns()
            elif selection == 4:
                self.all_players_tournament_report()
