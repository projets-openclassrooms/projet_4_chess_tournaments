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

    def __init__(self, name, firstname, birth, national_identification, score=0):
        self.name = name
        self.firstname = firstname
        self.date_of_birth = birth
        self.national_identification = national_identification
        self.score = score
        self.played_against = []
        self.player_uuid = str(uuid.uuid4())

    def __repr__(self):
        """Define the representation for a player object"""
        representation = (
            "Player('nom='"
            + self.name
            + "', prenom='"
            + self.firstname
            + "', une date de naissance='"
            + self.date_of_birth
            + "', identifier (INE)='"
            + self.national_identification
            + "')"
        )
        return representation

    def __str__(self):
        return f"Joueur {self.firstname} {self.name} - INE , {self.national_identification} (score: {self.score})"

    def full_name(self):
        """ """
        return f"- {self.firstname} {self.name}"
    def donnnes_completes(self):
        return f"id='{self.player_uuid}'nom='{self.name}', prenom=' {self.firstname} ', une date de naissance=' {self.date_of_birth} ', identifier (INE)='  {self.national_identification}"

    def __lt__(self, other):
        return self.score < other.score




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
            "name": self.name,
            "firstname": self.firstname,
            "birthday": self.date_of_birth,
            "national_identification": self.national_identification,
            "id": self.player_uuid,            
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
    def national_identification_exists(cls, national_identification):
        """Return existing national_identification or None if not exist"""
        players_saved = cls.get_players_saved()
        for player in players_saved:
            if national_identification == player.national_identification:
                return national_identification
        return None

    @classmethod
    def get_players_saved(self):
        """ interroge la base de données"""

        """:return: liste obj = players_saved"""

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
                    name = player["name"]
                    firstname = player["firstname"]
                    date_of_birth = player["birthday"]
                    national_identification = player["national_identification"]
                    players_to_return = Player(
                        name,
                        firstname,
                        date_of_birth,
                        national_identification,
                    )
                    # players_to_return.player_uuid = player_uuid
                    players_saved.append(players_to_return)
            return players_saved
        else:
            return players_saved

    @classmethod
    def get_player_by_id(cls, player_id):
        """:return: player selon id pour tournoi"""
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
                        national_identification = player["national_identification"]
                        player_to_return = Player(
                            player_uuid,
                            name,
                            firstname,
                            date_of_birth,
                            national_identification,
                        )
            return player_to_return



    @classmethod
    def restore_player(cls, player):
        """

        :param player:
        :return: player_to_return
        """
        national_identification = re.search(SEARCHING_INE, player)
        national_identification = national_identification.group(1)
        all_players = cls.get_players_saved()
        player_to_return = None
        for player in all_players:
            if player.national_identification == national_identification:
                player_to_return = player
                player_to_return.name = f"{player.name} + ({national_identification})"
                break
        return player_to_return


# player_store = {}
# nom = "Nom2"
# prenom = "prenom 2"
# date = "14/01/1989"
# identifiant = "id12355"

# player_one = Player(nom, prenom, date, identifiant)
# player_one_identity = player_one.national_identification  # INE
# dico_players = player_one.to_dict()

# print(dico_players)  #   dictionnaire pour json
# print(player_one.full_name())  # nom - prenom
# print(
#     player_one.national_identification_exists(player_one_identity)
# )  # None si non existant sinon INE
# # print(player_one.restore_player(player_one.full_name()))
# dico_players.save_new_player(file_players)
# dico_players.__getattribute__()  # sauvegarde du dictionnaire dans json

