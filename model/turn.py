"""Turn Model"""
import json
import os
import re
from datetime import datetime
from CONSTANTES import file_tournament, REPORT_FILE, TOURNAMENT_FOLDER

# TOURNAMENT_FOLDER = "data/tournaments"


class Turn:
    """Define a Turn as an object"""

    def __init__(
        self,
        round_name,
        start_round,
        end_round,
    ):
        self.round_name = round_name
        self.match_list = []
        self.start_round = start_round
        self.end_round = end_round

    def round_list(self):
        return [self.round_name, self.start_round, self.end_round, self.match_list]

    def get_round_list(self, match):
        self.matches = match

    @property
    def match_list(self):
        return self._match_list

    @match_list.setter
    def match_list(self, value):
        self._match_list = value

    @property
    def end_of_the_turn(self):
        return self._end_of_the_turn

    @end_of_the_turn.setter
    def end_of_the_turn(self, value):
        self._end_of_the_turn = value
        self.ending_turn = datetime.now()
