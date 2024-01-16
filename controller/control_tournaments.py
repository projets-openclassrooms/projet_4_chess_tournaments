import random

from CONSTANTES import COLOR, MAX_PLAYERS, STATUS_START, STATUS_PENDING, STATUS_ALL
from model import tournament
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
        description = self.tournament_view.ask_for_description()
        nb_turn = self.tournament_view.ask_for_nb_turn()
        players_saved = Player.get_players_saved()
        self.player_view.display_all_player_saved(players_saved)
        choix =""

        # initialise liste players du tournoi depuis players_saved
        players = []
        nb_players_chosen = len(players_saved)
        # loop pour atteindre 8 players max ou Q pour quitte
        while choix!="Q":
            choix = input(
                "Ajouter un joueur en indiquant son numéro ou Q pour quitter?"
            ).upper()
            if choix == "Q":
                break
            # verifier que index = choix (choix - 1 pour avoir index)

            index = int(choix) - 1
            if 0 <= index < nb_players_chosen and players_saved[index] not in players:
                players.append(players_saved[index])
            else:
                print("Veuillez entre un numéro valide")
        tournament = Tournament(
            name,
            location,
            description,
            players,
            ranking=[],
            turn_list=[],
            nb_turn=nb_turn,
        )
        tournament.save_tournament()
        print("Tournoi sauvegardé.")

    def display_tournaments(self):
        tournaments = Tournament.loads_tournament()
        self.tournament_view.display_all_tournaments(tournaments)

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
                # lancer un tournoi
                tournament = self.select_tournament(status=STATUS_START)  # status
                if tournament is None:
                    print("Vous n'avez pas choisi de tournoi.")
                else:
                    self.start_tournament(tournament)
            elif menu == "4":
                # rappeler un tournoi
                tournament = self.select_tournament(status=STATUS_PENDING)
                if tournament is None:
                    print("Vous n'avez pas choisi de tournoi.")
                else:
                    self.select_tournament(status=STATUS_PENDING)
            elif menu == "0":
                break
            else:
                print("Recommencez svp.")

    def list_tournament(self):
        tournaments = Tournament.loads_tournament()
        # print("players", players)
        self.tournament_view.display_all_tournaments(tournaments)

    def select_tournament(self, status=STATUS_ALL):
        """Allow to resume an unfinished tournament
        :return: restored
        """

        tournaments = Tournament.loads_tournament()
        self.tournament_view.display_all_tournaments(tournaments)
        choix = ""
        tournament = None
        while choix != "Q" and tournament is None:
            choix = input("Choisir le tournoi à executer ou Q pour quitter?").upper()
            if choix != "Q":
                # TODO verifier que l'index est pas de doublon
                index = int(choix) - 1
                tournament = tournaments[index]
            else:
                break
        return tournament

    def start_tournament(self, tournament):
        print(f"Début du tournoi {tournament}")
        print(f"{tournament.nb_turn} tours pour ce tournoi.")
        for tour in range(tournament.nb_turn):

            print(f"Pour le tour {tour+1}")
            if tour+1 == 1:
                self.turnview.display_match_list()
            # si tour n°1 (status not started)
            # recuperer la liste des players  du tournoi
            # randomiser les players et proposer un tuple de liste ([joueur 1, joueur 2])
            # avec generate_random_match()
            # proposer combinaisons de joueurs
            # affichage liste des joueurs tournoi
            # input saisie des scores
            # (joueur,scores) = input()
            # demander si saisie terminee
            # enregistrer resultat par serialisation
            # else tour n°2 proposer combinaisons de joueurs
            # affichage liste des joueurs tournoi
            # input saisie des scores
            # (joueur,scores) = input()
            # demander si saisie terminee
            # enregistrer resultat par serialisation

    def resume_tournament(self, tournament):
        print(f"Résumé du tournoi {tournament}")
        # si tour n°1 (status not started)
        # executer start_tournament(tournament)
        # else tour n°2 et status Pending
        # proposer combinaisons de joueurs
        # affichage liste des joueurs tournoi
        # input saisie des scores
        # (joueur,scores) = input()
        # demander si saisie terminee
        # enregistrer resultat par serialisation

    def generate_random_match(self, player_1=None, player_2=None):
        players_list = self.select_tournament(tournament, status=STATUS_START)
        random.sample(players_list)
        return [Match(player_1, player_2)]

    def get_chosen_tournament(self):
        """

        :rtype: object
        :return tournament or None
        """
        tournament = []
        all_tournaments = self.all_tournaments_name()
        if not all_tournaments:
            return None
        choice_control = False
        while not choice_control:
            choice = self.reportview.tournament_choice(all_tournaments)
            if not choice:
                return None
            choice_control = Tournament.control_name_exist(choice)
            if not choice_control:
                self.reportview.display_import_error()
                continue
            tournament = Tournament.get_tournament_info(choice)
        return tournament

    def get_turn_list(self, tournament_name):
        """part = turn (manche)
        :param tournament_name:
        :return: all_restored_turn or turn_list_saved
        """
        restored_turn = Turn.get_all_turn_files(tournament_name)
        if restored_turn:
            all_restored_turn = []
            for part in restored_turn:
                turn_list_saved = Turn.restore_turn(part)
                match_list = self.get_matches(turn_list_saved.match_list)
                turn_list_saved.match_list = match_list
                all_restored_turn.append(turn_list_saved)
            return all_restored_turn
        else:
            turn_list_saved = None
        return turn_list_saved

    def get_matches(self, matches_to_restore):
        """
        list of matches to restore

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

    def all_matches_and_turns(self):
        """Export a list of all matches
        from a selected tournament
        :return: export html or txt or csv"""
        tournament = self.get_chosen_tournament()
        if not tournament:
            return None
        tournament.turn_list = self.get_turn_list(tournament.name)
        title = [
            "Numéro du tour",
            "Nom Joueur",
            "INE du joueur",
            "Nom Opposant",
            "INE Opposant",
            "score joueur",
            "score opposant",
        ]
        data = []
        for turn in tournament.turn_list:
            for match in turn.match_list:
                player = match.player
                opponent = match.opponent
                player_score = match.player_score
                opponent_score = match.opponent_score
                if not match.match_result:
                    (player_score, opponent_score) = "Not Played"
                    opponent_score = "Not Played"
                match_list = [
                    turn.turn_nb,
                    player.name,
                    player.identifier,
                    opponent.name,
                    opponent.identifier,
                    player_score,
                    opponent_score,
                ]
                data.append(match_list)
        file_name = REPORT_FILE + "_" + tournament.name + "all_turn.csv"
        verification = self.report_control(file_name)
        if verification:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(title)
                writer.writerows(data)
            self.open_selected_report(file_name)
