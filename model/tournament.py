"""Define Tournament"""
import json
import os
import uuid
from datetime import datetime

from CONSTANTES import (STATUS_ALL, STATUS_END, STATUS_PENDING, STATUS_START,
                        file_tournament)

from .player import Player


class Tournament:
    """Define a tournament as an object,
    has a name, the location where it takes location,
    and a number total of turns, init nb_turn=4"""

    def __init__(
        self,
        name=None,
        location=None,
        description=None,
        players=[],
        nb_turn=4,
        turn=1,
        turn_list=[],
        ranking=[],
        comment=None,
        status=None,
        ending_date = None
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.description = description
        self.players = players
        self.nb_turn = nb_turn
        self._turn = turn
        self.turn_list = turn_list
        self._ranking = ranking
        self.comment = comment
        self.status = status
        self.starting_date = datetime.now()
        self.ending_date = ending_date

    def __repr__(self):
        """Define the representation of a tournament object
        :rtype: object
        """
        representation = (
            f"Tournament('name_of_tournament'={self.name}"
            + f"', location='{self.location}"
            + f"', description='{self.description}"
            + f"', status='{self.status}'"
        )

        return representation

    def __str__(self):
        return f"{self.name}"

    def get_tournament_id(self):
        return self.id

    def set_tournament_id(self):
        self.id = id

    def to_dict(self):
        """
        transforme donnees en dict pour json

        :rtype: dict
        :return:
        """
        if self.turn == 1:
            self.status = STATUS_START
        elif self.turn == self.nb_turn:
            self.status = STATUS_END

        else:
            self.status = STATUS_PENDING
        dict = {
            "id": self.id,
            "name_of_tournament": self.name,
            "location": self.location,
            "description": self.description,
            "turn": self._turn,
            "status": self.status,
            "turn_list": self.turn_list,
            "tournament_players": [p.player_uuid for p in self.players],
            "nb_turn": self.nb_turn,
            "ranking": [p.name for p in self._ranking],
            "comment": self.comment,
            "ended": self.ending_date if self.status == "ended" else None,
        }

        return dict

    def save_tournament(self):
        """ """
        new_tournament = self.to_dict()

        if os.path.exists(file_tournament):
            with open(file_tournament, "r") as file:
                all_tournaments = json.load(file)
                if "tournaments" in all_tournaments:
                    for tournament in all_tournaments["tournaments"]:
                        # check if already saved
                        if tournament["id"] == new_tournament["id"]:
                            all_tournaments["tournaments"].remove(tournament)

                    all_tournaments["tournaments"].append(new_tournament)
                else:
                    all_tournaments["tournaments"] = [new_tournament]
        else:
            all_tournaments = {"tournaments": [new_tournament]}

        with open(file_tournament, "w") as file:
            json.dump(all_tournaments, file, indent=4)

    @classmethod
    def loads_tournament(self, status=STATUS_ALL):
        # meme methode que players
        all_tournaments_returned = []
        with open(file_tournament) as file:
            all_tournaments_saved = json.load(file)
        if all_tournaments_saved.get("tournaments") is not None:
            for tournament in all_tournaments_saved["tournaments"]:
                t = Tournament()
                t.id = tournament["id"]
                t.name = tournament["name_of_tournament"]
                t.location = tournament["location"]
                t.turn = tournament["turn"]
                t.turn_list = tournament["turn_list"]
                # charge les objets players pour recreer objet
                t.players = []
                for player_id in tournament["tournament_players"]:
                    # print("player_id", player_id)
                    p = Player.get_player_by_id(player_id)
                    t.players.append(p)
                t.status = tournament["status"]
                t.nb_turn = tournament["nb_turn"]
                t.ranking = tournament["ranking"]
                t.comment = tournament["comment"]

                all_tournaments_returned.append(t)
        return all_tournaments_returned

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, value):
        self._turn = value

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = value

    @property
    def ended(self):
        self.ending_date = datetime.now()
        return self.ending_date
