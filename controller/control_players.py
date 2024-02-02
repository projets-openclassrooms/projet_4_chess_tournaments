"""Define Class Player Manager
    new_player with attributes

"""

import os
import uuid

from model.player import Player
from view.playerview import PlayerView
from view.reportview import ReportView
from view.tournamentview import TournamentView


class PlayerManager(object):
    def __init__(self):
        self.report_view = ReportView()
        self.tournament_view = TournamentView()
        self.player_uuid = str(uuid.uuid4())
        self.player_view = PlayerView()
        self.all_players = []

    def player_score(self):
        """Default created player's score."""
        self.score = 0.0

    def new_player(self):
        name = self.player_view.get_name()
        if not name:
            return None
        firstname = self.player_view.get_firstname()
        if not firstname:
            return None
        date_of_birth = self.player_view.get_birthdate()
        if not date_of_birth:
            return None
        create_identifier = True
        while create_identifier:
            national_identification = self.player_view.ask_national_identification()
            if not national_identification:
                return None
            control_identifier = Player.national_identification_exists(
                national_identification
            )
            if control_identifier:
                self.player_view.display_creation_error(control_identifier)
            elif not control_identifier:
                self.player_view.display_creation()
                player_uuid = self.player_uuid
                create_identifier = False
                score = self.player_score()  # default player score
                # played_against = []
        new_player = Player(
            name, firstname, date_of_birth, national_identification, player_uuid, score
        )
        new_player.save_new_player()
        print("Sauvegarde avec succes.")

    def display_players(self):
        players = Player.get_players_saved()
        players = sorted(players, key=lambda player: player.name, reverse=False)
        self.player_view.display_all_player_saved(players)

    def run_player(self):
        # all_player_saved = []
        menu = ""
        while menu != "0":

            menu = self.player_view.display_menu()
            if menu == "1":
                # nouveau joueur
                self.new_player()
            elif menu == "2":
                self.display_players()
            elif menu == "3":
                # Supprimer un joueur
                self.delete_player()
            elif menu == "4":
                self.tournament_view.display_menu()
            elif menu == "5":
                self.report_view.get_type_report()
            elif menu == "0":
                os.system(exit())
            else:
                if menu not in ["0", "1", "2", "3", "4", "5"]:
                    print("Saisie invalide. Svp entrer 0, 1, 2, 3, 4 ou 5.\n")
                    print("Recommencez svp.")

    def delete_player(self):
        pass
