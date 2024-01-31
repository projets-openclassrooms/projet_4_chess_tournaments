"""Define report manager
export csv, txt, or html"""

import csv

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
        tournament_index = int(input("Saisir le numéro du tournoi : "))
        choix = tournaments_data[tournament_index - 1]
        print(choix.name)

        if choix.status is None:
            for Round in choix.turn_list:
                print(f"- Nom: {Round['name']}")
                print(f"- Début : {Round['started']}")
                break

        else:
            for Round in choix.turn_list:
                print(f"- Nom: {Round['name']}")
                print(f"- Début : {Round['started']}")
                print(f"- Fin : {Round['ended']}")
            clear_screen()
            return self.run_report()

    def report_control(self):
        """

        :rtype: object
        :return boolean
        """
        self.report_tournaments.list_tournament()

        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)
        if len(tournaments_data) != 0:
            tournament_index = int(input("Saisir le numéro du tournoi : "))
            choix = tournaments_data[tournament_index - 1]
            if 1 <= choix <= len(tournaments_data):
                return choix
            else:
                print("Veuillez choisir un numéro valide.")
        else:
            self.report_view.display_empty()
            self.report_tournaments.run_tournament()
        self.report_view.display_create_report()

    def tournaments_matches_report(self):
        self.report_tournaments.list_tournament()

        tournaments_data = self.tournaments.loads_tournament(status=STATUS_ALL)
        tournament_index = int(input("Saisir le numéro du tournoi : "))
        choix = tournaments_data[tournament_index - 1]
        print(
            f"{'Nom du tournoi -':<16}{' Lieu':<9}{' - Description - ':<14}{'nb_Rounds - ':<4}{'Etat - ':<8}"
        )
        print(
            f"{choix.name:<14}{' - '}{choix.location:<8}{' - '}{choix.description:<12}\
                {' - '}{choix.nb_turn:<4}{' - '}{choix.status:<12}"
        )
        print("--------------------------")
        for Round in choix.turn_list:
            print(f"- Nom: {Round['name']}")
            print(f"- Début : {Round['started']}")
            print(f"- Fin : {Round['ended']}")
            print("- Matches :")
            for match_1, match_2 in Round["matches"]:
                print(
                    Player.get_player_by_id(match_1[0]).name,
                    "point :",
                    match_1[1],
                    colorise("Versus"),
                    Player.get_player_by_id(match_2[0]).name,
                    "point :",
                    match_2[1],
                )
            print("--------------------------")

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

    def save_report_tournaments(self):
        """Export a list of all tournaments saved"""

        all_tournaments = self.tournaments.loads_tournament(status=STATUS_ALL)
        title = [
            "N°",
            "Nom",
            "Statuts",
            "Nombre de tours",
            "Lieu",
            "Description",
        ]
        data = []
        for i, tournament in enumerate(all_tournaments, start=1):
            tournament_extract = [
                i,
                tournament.name,
                tournament.status,
                tournament.nb_turn,
                tournament.location,
                tournament.description,
            ]
            data.append(tournament_extract)
        file_name = REPORT_FILE + "all_tournaments.csv"
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(title)
            writer.writerows(data)
        self.report_view.display_create_report()

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
                self.save_report_tournaments()
            elif selection == 3:
                self.all_tournaments_by_name()

            elif selection == 4:
                self.all_players_tournament_report()

            elif selection == 5:
                self.tournaments_matches_report()

            else:
                if selection == 6:
                    break
