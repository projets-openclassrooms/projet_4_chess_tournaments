"""Define report manager
export csv, txt, or html"""

import csv
import os

from CONSTANTES import REPORT_FILE, STATUS_ALL
from controller.control_players import PlayerManager
from controller.control_tournaments import TournamentManager
from model.player import Player
from model.tournament import Tournament
from utils.settings import clear_screen, colorise
from view.reportview import ReportView

# REPORT_FILE = "data/report/"


class ReportManager:
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
        self.report_tournaments.list_tournament()

        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)

        tournament_index = int(
            input("Nom et Dates du tournoi à sélectionner\nSaisir numéro? ")
        )
        # for i, tournoi in enumerate(tournaments_data):
        for turn in tournaments_data[tournament_index +1]["turn_list"]:
            print("\t" + turn["name"] + turn["started"] + turn["ended"])
            # if i + 1 == tournament_index:
            #     if tournaments_data.ending_date is None:
            #
            #         print(
            #             f"{'N°-'},{'Nom du tournoi'},{'Date début - '},{'Date de fin.'}"
            #         )
            #         print(
            #             f"{i+1:<2} - {tournoi.name:<14}, {tournoi.starting_date:<10} - {'Pas fini.':<10}"
            #         )
            # else:
            #     print(f"{'N°-'},{'Nom du tournoi'},{'Date début - '},{'Date de fin.'}")
            #     print(
            #         f"{i+1:<2} - {tournoi.name:<14}, {tournoi.starting_date:<10} - {tournoi.ending_date:<10}"
            #     )

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
            return tournament_index

    def tournaments_matches_report(self):
        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)
        for i, tournoi in enumerate(tournaments_data):
            print(i + 1, tournoi)
        tournoi_choisi = int(input("Choisir le numéro du tournois : "))


        for tour in tournaments_data[tournoi_choisi-1].turn_list:

            for Round in tour:
                if Round is None:
                    continue
                for participant_id, score in Round:
                    # Process participant_id and score
                    participant_1_id = Player.get_player_by_id(participant_id).name
                    participant_2_id = Player.get_player_by_id(Round[1][0]).name
                    score_1 = Round[0][1]
                    score_2 = Round[1][1]

                    print(participant_1_id, score_1, "vs", participant_2_id, score_2)
            # for Round in tournaments_data[tournoi_choisi - 1].turn_list:
        #     if Round:
        #
        #     # if Round and Round.get("turn_list") == "matches":
        #     #     print(f"Tour n°{Round}")
        #         for participant_id, score in Round["matches"]:
        #             # Process participant_id and score
        #             participant_1_id = Player.get_player_by_id(participant_id).name
        #             participant_2_id = Player.get_player_by_id(Round["matches"][1][0]).name
        #             score_1 = Round["matches"][0][1]
        #             score_2 = Round["matches"][1][1]
        #
        #             print(participant_1_id, score_1, "vs", participant_2_id, score_2)
            else:
                print("Pas de matchs enregistrés.")
                clear_screen()
                continue

    def save_players_report(self):
        """Export a list of all players saved"""

        all_players = Player.get_players_saved()
        all_players = sorted(all_players, key=lambda player: player.name, reverse=False)

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
        # self.open_selected_report()
        self.report_view.display_create_report()

    def all_players_tournament_report(self):
        """Export a list of players from a selected tournament
        in alphabetic order"""
        self.report_tournaments.list_tournament()

        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)
        tournament_index = int(input("Saisir le numéro du tournoi : "))
        for i, tournoi in enumerate(tournaments_data):
            if i + 1 == tournament_index:
                players_by_id = tournoi.players

                print("Nom du tournoi : ", tournoi.name, colorise("\nJoueurs : "))
                sorted_players = sorted(
                    players_by_id, key=lambda classe: (classe.name, classe.firstname)
                )
                for player in sorted_players:
                    print(player.name, player.firstname)
            continue

        clear_screen()

    def run_report(self):
        """liste des joueurs par ordre alphabétique ;
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
                self.tournaments_matches_report()

            else:
                selection == 6
                break
