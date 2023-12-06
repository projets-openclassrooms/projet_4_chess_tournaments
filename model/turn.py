"""Turn Model"""
import json
import os
import re
from datetime import datetime

TOURNAMENT_FOLDER = "data/tournaments"


class Turn:
    """Define a Turn as an object"""

    def __init__(
        self,
        tournament_name,
        turn_nb,
        match_list,
        end_of_the_turn=False,
    ):
        self.tournament_name = tournament_name
        self.turn_nb = turn_nb
        self._match_list = match_list
        self._end_of_the_turn = end_of_the_turn
        self.starting_turn = None
        self.ending_turn = None
        self.save_turn_data()

    def __repr__(self):
        """Define the representation for a turn object"""
        representation = (
            "Turn(tournament_name='"
            + self.tournament_name
            + "', turn_nb='"
            + str(self.turn_nb)
            + "', match_list={},".format(self.match_list)
            + "matches_result={})".format(self._match_list)
        )
        return representation

    def __str__(self):
        representation = (
            "Le tour numéro: "
            + str(self.turn_nb)
            + "du tournoi: '"
            + self.tournament_name
            + "', les matchs qui le compose sont: {}".format(self.match_list)
        )
        return representation

    def to_dict(self):
        return {
            "tournament_name": self.tournament_name,
            "turn_nb": self.turn_nb,
            "match_list": self._match_list,
        }

    def save_turn_data(self):
        """
        json dumps tournaments informations
        :rtype: object

        """
        new_turn = self.to_dict()
        self.tournament_name = self.tournament_name.replace(" ", "")
        all_information = new_turn
        if self.starting_turn is None:
            self.starting_turn = datetime.now()
            all_information.update({"start": str(self.starting_turn)})
        else:
            all_information["start"] = str(self.starting_turn)
        if self.ending_turn:
            all_information["end"] = str(self.ending_turn)
        else:
            all_information.update({"end": None})
        file_name = "{}/{}_turn{}.json".format(
            TOURNAMENT_FOLDER, self.tournament_name, self.turn_nb
        )
        with open(file_name, "w") as file:
            json.dump(all_information, file, default=lambda x: x.to_dict())

    @classmethod
    def get_all_turn_files(cls, t_name):
        """

        :param t_name:
        :return: file_list
        """
        turn_file = rf"^data/tournaments/{t_name}_turn[0-9]{{0,99}}.json$"
        file_list = []
        for root, _, files in os.walk(TOURNAMENT_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path.replace("\\", "/")
                if re.match(turn_file, file_path):
                    file_list.append(file_path)
        return file_list

    @classmethod
    def restore_turn(cls, turn_to_restore):
        """

        :param turn_to_restore:
        :return: turn_to_return
        """
        path_control = os.path.exists(turn_to_restore)
        if path_control is True:
            with open(turn_to_restore, "r") as file:
                all_infos = json.load(file)
            t_name = all_infos["tournament_name"]
            turn_nb = all_infos["turn_nb"]
            match_list = all_infos["match_list"]
            turn_to_return = cls(t_name, turn_nb, match_list)
            turn_to_return.starting_turn = all_infos["start"]
            if all_infos["end"]:
                turn_to_return.ending_turn = all_infos["end"]
        else:
            turn_to_return = None
        return turn_to_return

    @property
    def match_list(self):
        return self._match_list

    @match_list.setter
    def match_list(self, value):
        self._match_list = value
        self.save_turn_data()

    @property
    def end_of_the_turn(self):
        return self._end_of_the_turn

    @end_of_the_turn.setter
    def end_of_the_turn(self, value):
        self._end_of_the_turn = value
        self.ending_turn = datetime.now()
        self.save_turn_data()
