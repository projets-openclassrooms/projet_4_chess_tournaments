"""Player Model"""
import json

import os
import re
from CONSTANTES import SEARCHING_INE, DATA_FOLDER, file_players, file_tournament
import uuid

# SEARCHING_INE = r"\((.*)\)"
# DATA_FOLDER = r"data/"  ##f"{ABSOLUTE_PATH}data/"
# file_tournament = f"{DATA_FOLDER}tournament.json"
# file_players = f"{DATA_FOLDER}players.json"


class Player(object):
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
        """ """
        return f"- {self.firstname} {self.name}"

    def __lt__(self, other):
        return self.score < other.score

    def get_player_id(self):
        return self.player_uuid

    def set_player_id(self):
        self.player_uuid = player_uuid

    def enlever(self, element):
        if element in self:
            self.remove(element)
            return True
        return False

    @classmethod
    def sauvegarder(cls, self):
        chemin = file_players
        with open(chemin, "w") as f:
            json.dump(self, f, indent=4)

        return True

    def to_dict(self):
        """ """
        return {
            "id": self.player_uuid,
            "name": self.name,
            "firstname": self.firstname,
            "birthday": self.date_of_birth,
            "national_identification": self.identifier,
        }

    def save_new_player(self):
        """
        Save a new player object to a JSON file.

        Args:
            file_players (str): The path to the JSON file where the players are stored.

        Returns:
            None
        """
        new_player = self.to_dict()

        if os.path.exists(file_players):
            with open(file_players, "r") as file:
                all_players = json.load(file)
                if "players" in all_players:
                    all_players["players"].append(new_player)
                else:
                    all_players["players"] = [new_player]
        else:
            all_players = {"players": [new_player]}

        with open(file_players, "w") as file:
            json.dump(all_players, file, indent=4)

    @classmethod
    def set_player_uuid(self):
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

        # all_players_saved = dict()
        players_saved = []
        path_control = os.path.exists(DATA_FOLDER)
        # if not path_control:
        if path_control is True:
            with open(file_players) as file:
                all_players_saved = json.load(file)
                # print("liste des joueurs ",all_players_saved)
            if all_players_saved.get("players") is not None:
                for player in all_players_saved["players"]:
                    # for player in all_players_saved:
                    # print(player)
                    player_uuid = player["id"]
                    name = player["name"]
                    firstname = player["firstname"]
                    date_of_birth = player["birthday"]
                    identifier = player["national_identification"]
                    players_to_return = Player(
                        player_uuid,
                        name,
                        firstname,
                        date_of_birth,
                        identifier,
                    )
                    # players_to_return.player_uuid = player_uuid
                    players_saved.append(players_to_return)
            return players_saved
        else:
            return players_saved

    @classmethod
    def get_player_by_id(cls, player_id):
        """:return: player_to_return"""
        player_to_return = None
        path_control = os.path.exists(DATA_FOLDER)
        # if not path_control:
        if path_control is True:
            with open(file_players) as file:
                file_json = json.load(file)
            if file_json.get("players") is not None:
                for player in file_json["players"]:
                    if player["id"] == player_id:
                        player_uuid = player["id"]
                        name = player["name"]
                        firstname = player["firstname"]
                        date_of_birth = player["birthday"]
                        identifier = player["national_identification"]
                        player_to_return = Player(
                            player_uuid,
                            name,
                            firstname,
                            date_of_birth,
                            identifier,
                        )
            return player_to_return

    @classmethod
    def get_serialized_player(cls, player_ident):
        """INE unique pour serialiser players

        :param player_ident:
        :return: player_to_return
        """
        path_control = os.path.exists(DATA_FOLDER)
        player_to_return = None
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
        player_to_return = None
        for player in all_players:
            if player.identifier == identifier:
                player_to_return = player
                player_to_return.name = f"{player.name} + ({identifier})"
                break
        return player_to_return


# player_store = {}
# nom = "Nom2"
# prenom = "prenom 2"
# date = "14/01/1989"
# identifiant = "id12355"

# player_one = Player(nom, prenom, date, identifiant)
# player_one_identity = player_one.identifier  # INE
# dico_players = player_one.to_dict()

# print(dico_players)  #   dictionnaire pour json
# print(player_one.full_name())  # nom - prenom
# print(
#     player_one.identifier_exists(player_one_identity)
# )  # None si non existant sinon INE
# # print(player_one.restore_player(player_one.full_name()))
# dico_players.save_new_player(file_players)
# dico_players.__getattribute__()  # sauvegarde du dictionnaire dans json
