"""Define Class Player Manager
    new_player with attributes

"""
import uuid, json

from model.player import Player
from view.playerview import PlayerView
from CONSTANTES import file_players


class PlayerManager(object):
    def __init__(self):
        self.player_view = PlayerView()
        self.all_players = []

    def player_score(self):
        """Default created player's score."""
        self.score = 0.0

    def new_player(self):
        name = self.player_view.ask_for_name()
        if not name:
            return None
        firstname = self.player_view.ask_for_firstname()
        if not firstname:
            return None
        birthday = self.player_view.ask_for_birthday()
        if not birthday:
            return None
        create_identifier = True
        while create_identifier:
            identifier = self.player_view.ask_national_identification()
            if not identifier:
                return None
            control_identifier = Player.identifier_exists(identifier)
            if control_identifier:
                self.player_view.display_creation_error(control_identifier)
            elif not control_identifier:
                self.player_view.display_creation()
                # player_id = Player.set_player_uuid()
                create_identifier = False
                score = self.player_score()  # default player score
                # played_against = []
        new_player = Player(name, firstname, birthday, identifier, score)
        # new_player.set_player_uuid()

        # print("new_player", new_player)

        # new_player = Player(player_id, name, firstname, birthday, identifier, score)
        new_player.save_new_player()
        print("Sauvegarde avec succes.")

    def modify_player(self):
        self.display_players()
        all_players = []
        self.all_players = Player.get_players_saved()
        # self.player_view.display_all_player_saved(self.all_players)
        all_players.append(self.all_players)
        if self.all_players:
            for key, value in all_players.items():
                if all_players[0][0] == value:
                    new_info = self.view.modification_player(value)
                    if new_info[0] == "1":
                        value["name"] = new_info[1]
                    elif new_info[0] == "2":
                        value["firstname"] = new_info[1]
                    elif new_info[0] == "3":
                        value["birthday"] = new_info[1]
                    elif new_info[0] == "4":
                        value["identifier"] = new_info[1]
        with open(file_players, "w") as my_file:
            json.dump(file_players, my_file, indent=4)
        return None

    def run_player(self):
        # all_player_saved = []
        menu = ""
        while menu != "0":
            menu = self.player_view.display_menu()
            if menu == "1":
                # nouveau joueur

                self.new_player()
            elif menu == "2":
                # Supprimer un joueur
                self.delete_player()

            elif menu == "3":
                # modifier joueur
                self.modify_player()
            elif menu == "4":
                self.display_players()
            elif menu == "0":
                break
            else:
                print("Recommencez svp.")

    def delete_player(self):
        self.display_players()

        delete_player = self.player_view.ask_for_delete()
        return delete_player

    def display_players(self):
        players = Player.get_players_saved()
        # print("players", players)
        self.player_view.display_all_player_saved(players)
