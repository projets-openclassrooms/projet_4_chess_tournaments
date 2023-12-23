"""Define Match view
quel joueur a les blancs?
Qui joue contre qui?
Qui gagne?
"""


class MatchView:
    def display_color(self, match_list_with_color):
        """

        :rtype: object
        """
        print("Première partie, Joueurs :" + " et leurs couleurs pour ce tour: ")
        for player, color in match_list_with_color.items():
            if color == "Blanc":
                print(f"{player} jouera les Blanc")
            else:
                print(f"{player} jouera les Noir")

    def display_already_played(self, match):
        print(
            f"\n--> Le match {match.player} VS {match.opponent} est deja joué"
            + f" Le joueur: {match.player} à un score de : {match.player_score}\n"
            + f"et le joueur: {match.opponent} un score de {match.opponent_score}\n"
        )

    def ask_result(self, match):
        print("\n" + str(match))
        end_turn = False
        while end_turn is False:
            match_result = input(
                "Qui est le vainqueur entre"
                + f" {match.player} \033[1;34;41mvs {match.opponent}\n "
                + f"\033[0;31m '1' pour {match.player}, "
                + f"'2' pour {match.opponent} ou "
                + "\033[0;31m 'e' pour déclarer une égalité. \n"
                + "(1/2/e/q) : "
            ).upper()
            if match_result == "1":
                print(str(match.player) + " est le vainqueur\n")
                match.player_score += 1
                end_turn = True
            elif match_result == "2":
                print(str(match.opponent) + " est le vainqueur\n")
                match.opponent_score += 1
                end_turn = True
            elif match_result == "E":
                print("C'est un égalité!\n")
                match.player_score += 0.5
                match.opponent_score += 0.5
                end_turn = True
            elif match_result == "Q":
                print("Fin du tournoi")
                return None
            else:
                print(match_result + " est invalide")
            match.match_result = (
                [match.player, match.player_score],
                [match.opponent, match.opponent_score],
            )
        return match
