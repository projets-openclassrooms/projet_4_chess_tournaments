import random

from CONSTANTES import COLOR, MAX_PLAYERS
from model.match import Match
from model.player import Player
from model.tournament import Tournament
from model.turn import Turn
from view.matchview import MatchView
from view.playerview import PlayerView
from view.tournamentview import TournamentView
from view.turnview import TurnView

from utils.settings import clear_console

"""Define controller about tournament
    choice of pairs
    create_tournament
    randomize for 1st turn
"""


# Constantes COLOR = ["Blanc", "Noir"]


class TournamentManager:
    """Define Tournament Manager"""

    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.turnview = TurnView()
        self.matchview = MatchView()
        self.tournament = None

    def create_tournament(self):
        """return self.tournament : New tournament with
        a name, a location, a list of players and
        a number of turns
        :param players_saved:
        :return: None"""
        # prompt user nom du tournoi, endroit, nombre de tours pour get liste des players
        name = self.tournament_view.ask_for_name()
        location = self.tournament_view.ask_for_location()
        nb_turn = self.tournament_view.ask_for_nb_turn()
        players_saved = Player.get_players_saved()
        self.player_view.display_all_player_saved(players_saved)

        # initialise liste players du tournoi depuis playeers_saved
        players = []
        list_of_players_t = []
        # print(type(players_saved))

        nb_players = len(players_saved)
        # loop pour atteindre 8 players max ou Q pour quitter
        while True:
            choix = input(
                "Ajouter un joueur en indiquant son numéro ou Q pour quitter?"
            ).upper()
            if choix == "Q":
                break
            # verifier que index = choix (choix - 1 pour avoir index)
            try:
                index = int(choix) - 1
                if 0 <= index < nb_players and players_saved[index] not in players:
                    list_of_players_t = players.append(players_saved[index])

                else:
                    print("Veuillez entre un numéro valide")

            except ValueError:
                print("Veuillez entre un numéro valide")

        # print(f"nombre de joueurs choisis {players} \n{list_of_players_t}")
        # print("nombre de parties saisies ", nb_turn)
        tournament = Tournament(
            name, location, players, ranking=[], turn_list=[], nb_turn=nb_turn
        )
        tournament.save_tournament()
        print("Tournoi sauvegardé.")

    def display_tournaments(self):
        tournaments = Tournament.loads_tournament()
        self.tournament_view.display_all_tournaments(tournaments)


    def create_player_list(self, players_saved):
        """

        :param players_saved:
        :return: renamed_player in players
        """
        players = []
        while len(players) < 2:
            players = self.tournament_view.select_players(players_saved)
            if players is None:
                return None
            elif len(players) % 2 == 0 and len(players) >= 2:
                break
        i = 1
        for player in players:
            renamed_player = f"{i} - {player.name} ({player.identifier})"
            player.name = renamed_player
            i += 1
        return players

    def define_first_turn(self):
        """

        :param players_saved:
        :return: first_turn

        define first turn
        :return: first_turn
        """

        ############ DEFINIR tournament.players
        players = Player.get_players_saved()
        tournament_players = players.copy()
        random.shuffle(tournament_players)
        first_match_list = []
        while len(tournament_players) != 0:
            player = tournament_players[0]
            opponent = tournament_players[1]
            match = Match(player, opponent)
            first_match_list.append(match)
            tournament_players.remove(player)
            tournament_players.remove(opponent)
        first_turn = Turn(self.tournament.name, self.tournament.turn, first_match_list)
        return first_turn

    def randomize_color(self, turn):
        """Define a color for one player per match"""
        result = {}
        for match in turn.match_list:
            player_color = random.choice(COLOR)
            result.update({match.player: player_color})
        self.matchview.display_color(result)

    def define_player_list(self, match_result):
        """Return a list of player with theirs score to sorting them
        :param match_result:
        :return: player_list
        """
        player_list = []
        for match in match_result:
            player = match.player
            player.score = match.player_score
            player_list.append(player)
            opponent = match.opponent
            opponent.score = match.opponent_score
            player_list.append(opponent)
        return player_list

    def sorting_by_score(self, current_turn):
        """

        :param current_turn:
        :return: current_turn with players_name_sorted
        """
        matches = self.draft_match_result(current_turn)
        if not matches:
            return None
        player_list = self.define_player_list(matches)
        players_name_sorted = sorted(player_list, reverse=True)
        self.tournament.ranking = players_name_sorted
        self.turnview.display_matching(self.tournament)
        return current_turn

    def draft_match_result(self, existing_turn):
        """Take and return the result from matches
        :param existing_turn:
        :return: existing_turn.match_list
        """
        match_list = existing_turn.match_list.copy()
        match_index = 0
        for match in match_list:
            if match.match_result:
                self.matchview.display_already_played(match)
            else:
                match_list[match_index] = self.matchview.ask_result(match)
                if not match_list[match_index]:
                    return None
                existing_turn.match_list = match_list
            match_index += 1
        return existing_turn.match_list

    def all_previous_matches(self):
        """return previous_matches to avoid a
        second match between two players
        :rtype: object
        :return previous_matches"""
        previous_matches = []
        for existing_turn in self.tournament.turn_list:
            previous = ()
            for match in existing_turn.match_list:
                previous = (match.player, match.opponent)
                previous_matches.append(previous)
        return previous_matches

    def next_match_list(self, new_match_list):
        """return next_match_list for next confrontations"""
        next_match_list = []
        for new_match in new_match_list:
            player = new_match[0]
            opponent = new_match[1]
            player_score = player.score
            opponent_score = opponent.score
            next_match = Match(player, opponent, player_score, opponent_score)
            next_match_list.append(next_match)
        return next_match_list

    def define_match_list(self, turn_nb):
        """return new_turn after first turn of tournament"""
        restored_turn = self.restore_turn(self.tournament.name, listing=True)
        for turn in restored_turn:
            if turn.turn_nb == turn_nb:
                return turn
        previous_matches = self.all_previous_matches()
        ranking = self.tournament.ranking.copy()
        new_match_list = []
        while len(ranking) != 0:
            opponent_position = 1
            if len(ranking) == 0:
                break
            for player in ranking:
                next_versus = ()
                try:
                    opponent = ranking[opponent_position]
                # that means he has played with everyone else
                except IndexError:
                    previous_matches = []
                next_versus = (player, opponent)
                if player == opponent:
                    opponent_position += 1
                    continue
                if next_versus in previous_matches:
                    opponent_position += 1
                    continue
                elif (next_versus[1], next_versus[0]) in previous_matches:
                    opponent_position += 1
                    continue
                else:
                    new_match_list.append(next_versus)
                    ranking.remove(player)
                    ranking.remove(opponent)
        matches = self.next_match_list(new_match_list)
        new_turn = Turn(self.tournament.name, self.tournament.turn, matches)
        return new_turn

    def run_tournament(self):
        """
        Run the tournament management system.

        Displays a menu to the user and allows them to select various options,
        such as creating a new tournament or resuming an existing one.

        :rtype: None
        :return:
        """
        menu = 0
        while menu != "0":
            menu = self.tournament_view.display_menu()
            if menu == "1":
                self.create_tournament()
            elif menu == "2":
                self.list_tournament()
            elif menu == "3":
                # recherche du tournoi existant dans la base
                tournament = self.select_tournament()
                if tournament == None:
                    print("Vous n'avez pas choisi de tournoi.")
                else:
                    self.start_tournament(tournament)
            elif menu == "4":
                self.restore_tournament()
            elif menu == "0":
                break
            else:
                print("Recommencez svp.")

    def list_tournament(self):
        tournaments = Tournament.loads_tournament()
        # print("players", players)
        self.tournament_view.display_all_tournaments(tournaments)

    def select_tournament(self):
        """Allow to resume an unfinished tournament
        :return: restored
        """
        tournaments = Tournament.loads_tournament()
        self.tournament_view.display_all_tournaments(tournaments)
        choix = ""
        tournament = None
        while choix != "Q" and tournament == None:
            choix = input("Choisir le tournoi à executer ou Q pour quitter?").upper()
            if choix != "Q":
                # TODO verifier que l'index est pas de doublon
                index = int(choix) - 1
                tournament = tournaments[index]
            else:
                break
        return tournament

    def start_tournament(self, tournament):
        print(f"Start du tournoi {tournament}")

    def restore_tournament(self):
        self.display_tournaments()
        list_tournament = self.tournament.loads_tournament()
        tournaments_input = int(input())
        for i in range(len(list_tournament)):
            if tournaments_input == str(list_tournament[i]["id"]):
                t = list_tournament[i]
                t = Tournament(t["id"])

                self.run_tournament()

    def restore_turn(self, tournament_name, listing=False):
        """

        :param tournament_name:
        :param listing:
        :return: turn_saved
        """
        restored_turn = Turn.get_all_turn_files(tournament_name)
        if restored_turn and not listing:
            for turn in restored_turn:
                turn_saved = Turn.restore_turn(turn)
                match_list = self.restore_matches(turn_saved.match_list)
                turn_saved.match_list = match_list
        elif restored_turn and listing:
            all_restored_turn = []
            for turn in restored_turn:
                turn_saved = Turn.restore_turn(turn)
                match_list = self.restore_matches(turn_saved.match_list)
                turn_saved.match_list = match_list
                all_restored_turn.append(turn_saved)
            return all_restored_turn
        else:
            turn_saved = None
        return turn_saved

    def restore_matches(self, matches_to_restore) -> object:
        """

        :rtype: object
        :return matches
        """
        matches = []
        for match in matches_to_restore:
            match_restored = Match.restore_match(match)
            player = Player.restore_player(match_restored.player)
            opponent = Player.restore_player(match_restored.opponent)
            match_restored.player = player
            match_restored.opponent = opponent
            matches.append(match_restored)
        return matches
