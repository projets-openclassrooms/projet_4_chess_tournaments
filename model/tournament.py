"""Define Tournament"""
import json
import os
import re
from datetime import datetime
from CONSTANTES import file_tournament


class Tournament:
    """Define a tournament as an object,
    has a name, the location where it takes location,
    and a number total of turns, init nb_turn=4"""

    def __init__(
        self,
        name,
        location,
        players,
        nb_turn=4,
        turn=1,
        turn_list=None,
        ranking=None,
        save=True,
        comment=None,
        finished=False,
    ):
        self.name = name
        self.location = location
        self.players = players
        self.nb_turn = nb_turn
        self._turn = turn
        self.turn_list = turn_list
        self._ranking = ranking
        self.comment = comment
        self._finished = finished
        self.starting_date = None
        self.ending_date = None
        if save:
            self.save_tournament()

    def __repr__(self):
        """Define the representation of a tournament object
        :rtype: object
        """
        player_list = []
        if self.players:
            for player in self.players:
                player_list.append(player.name)
        representation = (
            f"Tournament(name='{self.name}"
            + f"', lieu='{self.location}"
            + f"', players={player_list}, nb_turn='"
            + str(self.nb_turn)
            + f"', turn='{str(self.turn)}"
            + f"', turn_list={self.turn_list})"
        )
        return representation

    def to_dict(self):
        """
        transforme donnees en dict pour json

        :rtype: dict
        :return:
        """
        return {
            "name_of_tournament": self.name,
            "location": self.location,
            "turn": self._turn,
            "tournament_players": [p.identifier for p in self.players],
            "total_of_turn": self.nb_turn,
            "ranking": [p.name for p in self._ranking],
            "comment": self.comment,
        }

    def save_tournament(self):
        """ """
        new_tournament = self.to_dict()
        tournament_name = self.name
        all_information = new_tournament
        if not self.starting_date:
            self.starting_date = datetime.now()
            all_information.update({"starting_date": str(self.starting_date)})
        else:
            all_information["starting_date"] = str(self.starting_date)
        if self.ending_date:
            all_information.update({"ending_date": str(self.ending_date)})
        else:
            all_information.update({"ending_date": None})
        # tournament_file = TOURNAMENT_FOLDER + "/" + tournament_name + ".json"
        # tournament_file = tournament_file.replace(" ", "")
        with open(file_tournament, "w") as file:
            json.dump(all_information, file)

    @classmethod
    def control_finished(cls, tournament):
        path_control = os.path.exists(tournament)
        if path_control is True:
            with open(tournament, "r") as file:
                all_infos = json.load(file)
                if all_infos["ending_date"]:
                    return tournament
                else:
                    return None
        else:
            return None

    @classmethod
    def get_all_tournament_names(cls, with_finished=False):
        file_list = []
        file_list.append(file_tournament)
        # for root, _, files in os.walk(file_tournament):
        #     for file in files:
        #         file_path = os.path.join(root, file)
        #         file_path = file_path.replace("\\", "/")
        #         if re.match(file_tournament, file_path):
        #             file_path = file_path.replace(TOURNAMENT_FOLDER, "")
        #             file_path = file_path.replace(".json", "")
        #             file_list.append(file_path)
        final_list = []
        if with_finished:
            for tournament in file_list:
                tournament_control = cls.control_finished(tournament)
                if not tournament_control:
                    final_list.append(tournament)
            return final_list
        else:
            return file_list

    @classmethod
    def control_name_exist(cls, tournament_name):
        tournaments_saved = cls.get_all_tournament_names()
        if tournament_name in tournaments_saved:
            return True
        else:
            return False

    @classmethod
    def get_tournament_info(cls, name):
        """

        :param name:
        :return: saved_tournament or None
        """
        tournament_file = file_tournament
        path_control = os.path.exists(tournament_file)
        if path_control is True:
            with open(tournament_file, "r") as file:
                all_infos = json.load(file)
            name = all_infos["name_of_tournament"]
            location = all_infos["location"]
            players = all_infos["tournament_players"]
            nb_turn = all_infos["total_of_turn"]
            ranking = all_infos["ranking"]
            turn = all_infos["turn"]
            turn_list = []
            saved_tournament = cls(
                name=name,
                location=location,
                players=players,
                nb_turn=nb_turn,
                turn=turn,
                turn_list=turn_list,
                ranking=ranking,
                save=False,
            )
            saved_tournament.starting_date = all_infos["starting_date"]
            if all_infos["ending_date"]:
                saved_tournament.ending_date = all_infos["ending_date"]
                saved_tournament.comment = all_infos["comment"]
        else:
            return None
        return saved_tournament

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, value):
        self._turn = value
        self.save_tournament()

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = value
        self.save_tournament()

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value
        if self._finished:
            self.ending_date = datetime.now()
        self.save_tournament()
