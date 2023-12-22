"""Player Model"""
import json
import os
import re
from CONSTANTES import SEARCHING_INE, DATA_FOLDER, file_players, file_tournament
import uuid

# class Example:
#     def __init__(self,param1,param2):
#         self.param1 = param1
#         self.param2 = param2
#     @classmethod
#     def my_method(cls,param1,param2):
#         return cls(param1,param2)
#
# example = Example.my_method(1,2)
# print(example)
# class GFG:
# 	def __lt__(self, other):
# 		return "YES"
# obj1 = GFG()
# obj2 = GFG()
#
# print(obj1 < obj2)
# print(type(obj1 < obj2))


class Player:
    """Define player as an object:
    A player has a name, a firstname, a date_of_birth and a national identifier chess, un score à 0
    """

    def __init__(self, name, firstname, birth, identifier, score=0):
        self.player_uuid = str(uuid.uuid4())
        self.name = name
        self.firstname = firstname
        self.date_of_birth = birth
        self.identifier = identifier
        self.score = score
        self.played_against = []

    def __repr__(self):
        """Define the representation for a player object"""
        representation = (
            "Player(nom='"
            + self.name
            + "', prenom='"
            + self.firstname
            + "', une date de naissance='"
            + self.date_of_birth
            + "', identifier (INE)='"
            + self.identifier
            + "')"
        )
        return representation

    def __str__(self):
        return f"Le joueur {self.name} - INE , {self.identifier} (score: {self.score})"
    
    def full_name(self):
        return f"- {self.first_name} {self.name}"
    
    def __lt__(self, other):
        return self.score < other.score

    def to_dict(self):
        return {
            "id": self.player_uuid,
            "name": self.name,
            "firstname": self.firstname,
            "birthday": self.date_of_birth,
            "national_identification": self.identifier,
        }

    def save_new_player(self):
        """
        json dumps players

        """
        new_player = self.to_dict()
        #print(new_player)
        path_control = os.path.exists(DATA_FOLDER)
        if path_control is True:
            with open(file_players, "r") as file:
                all_players = json.load(file)
                if all_players.get("players") is not None:
                    all_players["players"].append(new_player)
                else:
                    all_players = {"players": [new_player]}
        else:
            all_players = {"players": [new_player]}
        with open(file_players, "w") as file:
            json.dump(all_players, file)

    @classmethod
    def set_player_uuid():
        player_uuid = uuid.uuid4()
        return player_uuid

    @classmethod
    def identifier_exists(cls, identifier):
        """Return existing identifier or None if not exist"""
        players_saved = cls.get_players_saved()
        for player in players_saved:
            if identifier == player.identifier:
                return identifier
        return None

    @classmethod
    def get_players_saved(self):
        # all_players_saved = {}

        """:return: players_saved"""

        # print(all_players_saved)
        # all_players_saved = dict()
        players_saved = []
        path_control = os.path.exists(DATA_FOLDER)
        # if not path_control:
        if path_control is True:
            with open(file_players) as file:
                all_players_saved = json.load(file)
            if all_players_saved.get("players") is not None:
                for player in all_players_saved["players"]:
                # for player in all_players_saved:
                    #print(player)
                    player_uuid = player["id"]
                    name = player["name"]
                    firstname = player["firstname"]
                    date_of_birth = player["birthday"]
                    identifier = player["national_identification"]
                    players_to_return = Player(
                        name,
                        firstname,
                        date_of_birth,
                        identifier,
                    )
                    players_to_return.player_uuid = player_uuid
                    players_saved.append(players_to_return)
            return players_saved
        else:
            return players_saved

    @classmethod
    def get_serialized_player(cls, player_ident):
        """INE unique pour serialiser players

        :param player_ident:
        :return: player_to_return
        """
        path_control = os.path.exists(DATA_FOLDER)
        if path_control is True:
            with open(file_players, "r") as file:
                all_players_saved = json.load(file)
            for player in all_players_saved["players"]:
                ident = player["national_identification"]
                if player_ident == ident:
                    name = player["name"] + " (" + ident + ")"
                    firstname = player["firstname"]
                    birthday = player["birthday"]
                    played_against = player["played_against"]
                    player_to_return = Player(
                        name, firstname, birthday, ident, played_against
                    )
        return player_to_return

    @classmethod
    def restore_player(cls, player):
        """

        :param player:
        :return: player_to_return
        """
        identifier = re.search(SEARCHING_INE, player)
        identifier = identifier.group(1)
        all_players = cls.get_players_saved()
        for player in all_players:
            if player.identifier == identifier:
                player_to_return = player
                player_to_return.name = player.name + " (" + identifier + ")"
                break
        return player_to_return
