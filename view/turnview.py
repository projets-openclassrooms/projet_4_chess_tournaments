"""Define Turn View"""


class TurnView:
    def display_match_list(self, turn=1):
        """
        display turn num. and opponents' list

        :param turn: turn_nb
        """
        print(
            f"Pour la manche {turn}:\n"
            + "Voici la liste des joueurs qui vont s'affronter:\n"
        )
        for match in turn.matchs:
            print(f"{match.player} VS {match.opponent}\n")
        # print(f"Manche {turn.turn_nb}:")

    def display_matching(self, tournament_data):
        """

        :param tournament_data: turn_nb player.name player.score
        """
        turn_nb = tournament_data.turn
        print(f"\nFin de la manche {turn_nb}:")

        print("\nVoici le classement actuel: ")
        sorted_player = tournament_data.ranking
        for player in sorted_player:
            print(f"{player.name} avec {player.score} points")
