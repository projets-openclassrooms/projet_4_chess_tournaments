"""Define a match"""


# TOURNAMENT_FOLDER = "data/tournaments"


class Match:
    """Define a Match as an object"""

    def __init__(
        self,
        player,
        opponent,
        player_score=0,
        opponent_score=0,
        match_result=None,
    ):
        self.player = player
        self.opponent = opponent
        self.player_score = player_score
        self.opponent_score = opponent_score
        self.match_result = match_result

    def __repr__(self):
        """Define the representation of match object,
        for player object, we will display only his name"""
        representation = (
            "Match(player=' "
            + str(self.player)
            + " ',opponent='"
            + str(self.opponent)
            + " ',player_score='"
            + str(self.player_score)
            + " ',opponent_score='"
            + str(self.opponent_score)
            + "')"
        )
        return representation

    def __str__(self):
        return "Le match entre " + str(self.player) + " et " + str(self.opponent)

    def to_dict(self):
        return {
            "result": [
                (
                    [self.player.player_uuid, self.player_score],
                    [self.opponent.player_uuid, self.opponent_score],
                )
            ]
        }

    @classmethod
    def resume_match(cls, dict_match):
        player = dict_match["player"]
        opponent = dict_match["opponent"]
        p_score = dict_match["player_score"]
        o_score = dict_match["opponent_score"]
        m_result = dict_match["match_result"]
        resumed_match = cls(player, opponent, p_score, o_score, m_result)
        return resumed_match
