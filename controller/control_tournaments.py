import random

from CONSTANTES import COLOR
from model.match import Match
from model.player import Player
from model.tournament import Tournament
from model.turn import Turn
from view.matchview import MatchView
from view.playerview import PlayerView
from view.tournamentview import TournamentView
from view.turnview import TurnView

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

    def create_tournament(self, players_saved):
        """return self.tournament : New tournament with
        a name, a location, a list of players and
        a number of turns
        :param players_saved:
        :return: self.tournament"""
        all_tournaments_names = Tournament.get_all_tournament_names()
        name = self.tournament_view.ask_for_name(all_tournaments_names)
        control_name = Tournament.control_name_exist(name)
        if name is None:
            return None
        elif control_name is True:
            self.tournament_view.display_saving_error()
            return None
        location = self.tournament_view.ask_for_location()
        if location is None:
            return None
        players = self.create_player_list(players_saved)
        if not players:
            return None
        empty_list = []
        self.tournament = Tournament(
            name, location, players, ranking=empty_list, turn_list=empty_list
        )
        nb_turn = self.tournament_view.ask_for_nb_turn(players)
        if nb_turn is None:
            return None
        self.tournament.nb_turn = nb_turn
        return self.tournament

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
        players_saved
        starting_turn
        ending_turn
        comment

        :rtype: object
        :return:
        """
        menu = ""
        while menu != "0":
            menu = self.tournament_view.display_menu()
            if menu == "1":
                self.select_tournament()
                #self.define_first_turn()
                # self.create_tournament(Player.get_players_saved())
            elif menu == "2":
                # recherche du tournoi existant dans la base
                self.select_tournament()
            elif menu == "0":
                break
            else:
                print("Recommencez svp.")

        # self.tournament = None
        # players_saved = Player.get_players_saved()
        # if not players_saved:
        #     self.tournament_view.ask_for_players()
        #     return None
        # ask_for_new = self.tournament_view.ask_to_continue()
        # if ask_for_new:
        #     self.tournament = self.create_tournament(players_saved)
        # elif not ask_for_new:
        #     self.tournament = self.select_tournament()
        # else:
        #     return None
        # if not self.tournament:
        #     return None
        # for _ in range(self.tournament.turn, self.tournament.nb_turn + 1):
        #     if self.tournament.turn == 1:
        #         starting_turn = self.define_first_turn()
        #     else:
        #         starting_turn = self.define_match_list(self.tournament.turn)
        #     self.turnview.display_match_list(starting_turn)
        #     self.randomize_color(starting_turn)
        #     ending_turn = self.sorting_by_score(starting_turn)
        #     if ending_turn is None:
        #         return None
        #     ending_turn.end_of_the_turn = True
        #     self.tournament.turn_list.append(ending_turn)
        #     if self.tournament.turn < self.tournament.nb_turn:
        #         self.tournament.turn = self.tournament.turn + 1
        # comment = self.tournament_view.ask_to_comment()
        # self.tournament.comment = comment
        # self.tournament.finished = True

    def select_tournament(self):
        """Allow to resume an unfinished tournament
        :return: restored
        """
        all_path = Tournament.get_all_tournament_names(with_finished=True)
        choice = self.tournament_view.select_previous_tournament(all_path)
        if choice is None:
            return None
        path_control = Tournament.control_name_exist(choice)
        if path_control:
            restored = self.restore_tournament(choice)
            if not restored:
                return None
        else:
            self.tournament_view.display_import_error()
            return None
        return restored

    def restore_tournament(self, tournament_name):
        t_restored = Tournament.get_tournament_info(tournament_name)
        tournament_player = []
        for player in t_restored.players:
            player_found = Player.get_serialized_player(player)
            tournament_player.append(player_found)
        t_restored.players = tournament_player
        tournament_ranking = []
        for player in t_restored.ranking:
            player_restored = Player.restore_player(player)
            tournament_ranking.append(player_restored)
        t_restored.ranking = tournament_ranking
        if t_restored.turn > 1:
            turn_list = self.restore_turn(t_restored.name, listing=True)
            t_restored.turn_list = turn_list
        return t_restored

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
