"""Define Class Player Manager
    new_player with attributes

"""
import uuid, json

from model.player import Player
from view.playerview import PlayerView
from CONSTANTES import file_players 


class PlayerManager:
    def __init__(self):
        self.player_view = PlayerView()
        self.all_players = []

    def player_score(self):
        """Default created player's score."""
        self.score = 0.0

    def new_player(self):
        another_add = True
        new_player = None
        while another_add:
            self.all_players = Player.get_players_saved()
            self.player_view.display_all_player_saved(self.all_players)
            if self.all_players:
                another_add = self.player_view.add_again()
                if not another_add:
                    break
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
                    # player_uuid = Player.set_player_uuid()
                    create_identifier = False
                    score = 0
                    played_against = []
            new_player = Player(name, firstname, birthday, identifier, score)
            print(new_player)

            # new_player = Player(player_id, name, firstname, birthday, identifier, score)
            new_player.save_new_player()
            self.all_players = Player.get_players_saved()
        return new_player

    def modify_player(self):
        all_players = []
        self.all_players = Player.get_players_saved()
        self.player_view.display_all_player_saved(self.all_players)
        if self.all_players:
            for key, value in all_players[player].items():
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
        self.new_player()
        all_player_saved = Player.get_players_saved()
        return all_player_saved
    
    def delete_player(self):
        self.modify_player()
        delete_player  = self.player_view.ask_for_delete()
        return delete_player
    
    def display_players(self):
        self.modify_player()
        modified_player = self.player_view.display_player()
        return modified_player
