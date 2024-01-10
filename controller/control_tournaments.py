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
        description = self.tournament_view.ask_for_description()
        nb_turn = self.tournament_view.ask_for_nb_turn()
        players_saved = Player.get_players_saved()
        self.player_view.display_all_player_saved(players_saved)

        # initialise liste players du tournoi depuis players_saved
        players = []

        # loop pour atteindre 8 players max ou Q pour quitte
        while len(players) < MAX_PLAYERS:
            choix = input(
                "Ajouter un joueur en indiquant son numéro ou Q pour quitter?"
            ).upper()
            if choix == "Q":
                break
            # verifier que index = choix (choix - 1 pour avoir index)

            index = int(choix) - 1
            if 0 <= index < len(players) and players_saved[index] not in players:
                players.append(players_saved[index])
            else:
                print("Veuillez entre un numéro valide")
        tournament = Tournament(
            name, location, description, players, ranking=[], turn_list=[], nb_turn=nb_turn
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
                # recherche du tournoi existant dans la base
                tournament = self.select_tournament() #status
                if tournament is None:
                    print("Vous n'avez pas choisi de tournoi.")
                else:
                    self.start_tournament(tournament)
            elif menu == "4":
                tournament = self.select_tournament()
                if tournament is None:
                    print("Vous n'avez pas choisi de tournoi.")
                else:                
                    self.restore_turn(tournament)
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
        print(tournament.nb_turn)
        for tour in range(tournament.nb_turn):
            print(f"Pour {tour}")
        
    def resume_tournament(self, tournament):
        print(f"resume du tournoi {tournament}")
