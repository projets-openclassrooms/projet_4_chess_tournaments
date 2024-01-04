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

    def get_chosen_tournament(self):
        """

        :rtype: object
        :return tournament or None
        """
        tournament = ""
        all_tournaments = self.all_tournaments_name()
        if not all_tournaments:
            return None
        choice_control = False
        while not choice_control:
            choice = self.reportview.tournament_choice(all_tournaments)
            if not choice:
                return None
            choice_control = Tournament.control_name_exist(choice)
            if not choice_control:
                self.reportview.display_import_error()
                continue
            tournament = Tournament.get_tournament_info(choice)
        return tournament

    def get_turn_list(self, tournament_name):
        """part = turn (manche)
        :param tournament_name:
        :return: all_restored_turn or turn_list_saved
        """
        restored_turn = Turn.get_all_turn_files(tournament_name)
        if restored_turn:
            all_restored_turn = []
            for part in restored_turn:
                turn_list_saved = Turn.restore_turn(part)
                match_list = self.get_matches(turn_list_saved.match_list)
                turn_list_saved.match_list = match_list
                all_restored_turn.append(turn_list_saved)
            return all_restored_turn
        else:
            turn_list_saved = None
        return turn_list_saved

    def get_matches(self, matches_to_restore):
        """
        list of matches to restore

        :rtype: object
        :return matches
        """
        matches = []
        for match in matches_to_restore:
            match_restored = Match.restore_match(match)
            player = Player.restore_player(match_restored.player)
            opponent = Player.restore_player(match_restored.opponent)
            match_restored.player = player
            match_restored.opponent = opponent
            matches.append(match_restored)
        return matches

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
            print("Verification échoue. Rapport non créé.")

    def all_matches_and_turns(self):
        """Export a list of all matches
        from a selected tournament
        :return: export html or txt or csv"""
        tournament = self.get_chosen_tournament()
        if not tournament:
            return None
        tournament.turn_list = self.get_turn_list(tournament.name)
        title = [
            "Numéro du tour",
            "Nom Joueur",
            "INE du joueur",
            "Nom Opposant",
            "INE Opposant",
            "score joueur",
            "score opposant",
        ]
        data = []
        for turn in tournament.turn_list:
            for match in turn.match_list:
                player = match.player
                opponent = match.opponent
                player_score = match.player_score
                opponent_score = match.opponent_score
                if not match.match_result:
                    (player_score, opponent_score) = "Not Played"
                    opponent_score = "Not Played"
                match_list = [
                    turn.turn_nb,
                    player.name,
                    player.identifier,
                    opponent.name,
                    opponent.identifier,
                    player_score,
                    opponent_score,
                ]
                data.append(match_list)
        file_name = REPORT_FILE + "_" + tournament.name + "all_turn.csv"
        verification = self.report_control(file_name)
        if verification:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(title)
                writer.writerows(data)
            self.open_selected_report(file_name)

    def all_players_report(self):
        """Export a list of all players saved"""
        
        all_players = Player.get_players_saved()
        title = ["Nom", "Prénom", "Date de Naissance", "identifier"]
        data = []
        for player in all_players:
            player_extract = [
                player.name,
                player.firstname,
                player.date_of_birth,
                player.identifier,
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
            print("Verification échoue. Rapport non trouvé.")

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
