"""Define Class Player Manager
    new_player with attributes

"""
import uuid, json

from model.player import Player
from view.playerview import PlayerView


from utils.settings import clear_console


class PlayerManager(object):
    def __init__(self):
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

    def modify_player(self):
        self.display_players()
        players_to_modify = Player.get_players_saved()
        player_modified = False
        self.player_view.ask_to_modify_player(players_to_modify)
        i = 1
        for player in players_to_modify:
            print(i, "player", player.full_name())
            i += 1
            self.player_view.select_player(player[i])
        self.player_view.get_name()
        self.player_view.get_firstname()
        self.player_view.ask_national_identification()

    def delete_player(self):
        self.display_players()
        players_to_delete = Player.get_players_saved()
        player_deleted = False
        self.player_view.ask_to_delete_player(players_to_delete)
        i = 1
        for player in players_to_delete:
            print(i, "player", player.full_name())

    def display_players(self):
        players = Player.get_players_saved()
        self.player_view.display_all_player_saved(players)

    def run_player(self):
        # all_player_saved = []
        menu = ""
        while menu != "0":
            clear_console()

            menu = self.player_view.display_menu()
            if menu == "1":
                # nouveau joueur
                self.new_player()
            elif menu == "2":
                self.display_players()

            # elif menu == "3":
            #     # Supprimer un joueur
            #     self.delete_player()
            # elif menu == "4":
            #     # modifier joueur
            #     self.modify_player()

            elif menu == "0":
                break
            else:
                print("Recommencez svp.")
