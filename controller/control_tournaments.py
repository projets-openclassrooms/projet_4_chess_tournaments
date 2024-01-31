import random
from datetime import datetime

from CONSTANTES import STATUS_ALL, STATUS_END, STATUS_PENDING, STATUS_START
from model.player import Player
from model.tournament import Tournament
from utils.settings import clear_console, clear_screen, colorise, is_odd
from view.playerview import PlayerView
from view.tournamentview import TournamentView

"""Define controller about tournament
    choice of pairs
    create_tournament
    randomize for 1st turn
"""


# Constantes COLOR = ["Blanc", "Noir"]


class TournamentManager:
    """Define Tournament Manager"""

    def __init__(self):
        self.Tournaments = Tournament()
        self.status = None
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()

        self.tournament = None
        self.ending_date = datetime.now()

    def create_tournament(self):
        # prompt users tournoi resultat liste tournament de players, lieu,...
        name = self.tournament_view.get_name()
        location = self.tournament_view.get_location()
        description = self.tournament_view.get_description()
        nb_turn = self.tournament_view.get_nb_turn()
        players_saved = Player.get_players_saved()
        self.player_view.display_all_player_saved(players_saved)
        choix = ""
        combien = int(input("Combien de participants? "))

        # initialise liste players du tournoi depuis players_saved
        players = []
        nb_players = len(players_saved)
        i = 0
        # loop pour atteindre 8 players max ou Q pour quitter
        while combien != i:
            choix = input(
                "Ajouter un joueur en indiquant son numéro ou Q pour quitter?"
            ).upper()
            i += 1

            if choix == "Q" or i == combien + 1:
                break
            try:
                index = int(choix) - 1
                if 0 <= index < nb_players and players_saved[index] not in players:
                    players.append(players_saved[index])

                elif is_odd(players):
                    self.tournament_view.incomplete_list(players)
                    return
                else:
                    self.tournament_view.display_error()
            except ValueError:
                self.tournament_view.display_error()
            for player in players:
                print(f"{player.name} sélectionné.")
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
                tournament_to_choose = self.select_tournament(status=STATUS_START)
                if not tournament_to_choose:
                    return
                # print(f"tournoi sélectionné : {tournament.name}, {tournament.players}")
            elif menu == "4":
                # rappeler un tournoi
                tournament_to_choose = self.select_tournament(status=STATUS_PENDING)
                # si aucun tournoi donc break
                if not tournament_to_choose:
                    return
                print(f"tournoi sélectionné : {tournament_to_choose.name}")
                self.start_tournament(tournament_to_choose)
            elif menu == "0":
                break
            else:
                print("Recommencez svp.")

    def list_tournament(self):
        tournaments = Tournament.loads_tournament()
        # print("players", players)
        self.tournament_view.display_all_tournaments(tournaments)
        clear_screen()

    def select_tournament(self, status=STATUS_ALL):
        """Allow to resume an unfinished tournament STATUS_START or STATUS_PENDING
        :return: restored
        """
        filtered_tournaments = []

        tournaments_data = Tournament.loads_tournament()
        # print(tournaments_data)
        #
        # self.tournament_view.display_all_tournaments(tournaments_data)
        # Filter the list of tournaments to only include those with a status "not started"
        if status == STATUS_START:
            filtered_tournaments = [
                tournament_to_choose
                for tournament_to_choose in tournaments_data
                if tournament_to_choose.status == STATUS_START
            ]
        elif status == STATUS_PENDING:
            filtered_tournaments = [
                tournament_to_choose
                for tournament_to_choose in tournaments_data
                if tournament_to_choose.status == STATUS_PENDING
            ]
        else:
            status = STATUS_ALL
            filtered_tournaments = [
                tournament_to_choose
                for tournament_to_choose in tournaments_data
                if tournament_to_choose.status == status
            ]
        self.tournament_view.display_all_tournaments(filtered_tournaments)

        while True:
            choix = input("Choisir le tournoi ou Q pour quitter? ").upper()
            if choix == "Q":
                # si aucun tournoi donc return menu

                return
            try:
                index = int(choix) - 1
                if 0 <= index < len(filtered_tournaments):
                    tournament_to_choose = filtered_tournaments[index]
                    clear_console()
                    break
                else:
                    print("Index invalide")
            except ValueError:
                print("Entrez un index valide")

        print(f"tournoi sélectionné : {tournament_to_choose.name}")
        self.start_tournament(tournament_to_choose)

        return tournament_to_choose

    def start_tournament(self, tournaments_data):
        # recuperer fromdict tournament
        # recuperer fromdict players
        # recuperer la liste des players  du tournoi
        # print(type(tournaments_data))

        # randomiser les players et proposer un tuple de liste ([joueur 1, joueur 2])
        # Génération d'un match aléatoire avec generate_random_match()

        # proposer combinaisons de joueurs
        # affichage liste des joueurs tournoi
        score2 = 0

        # input saisie des scores
        # (joueur,scores) = input()
        # demander si saisie terminee
        # enregistrer resultat par serialisation
        # else tour n°2 proposer combinaisons de joueurs
        print(f"Début du tournoi {tournaments_data.name}")
        # self.tournament_view.display_points()
        print(f"{tournaments_data.nb_turn} tours pour ce tournoi.")
        # boucle tant que fin de saisie != Q
        clear_console()

        for tour in range(tournaments_data.nb_turn):
            tour_obj = {
                "name": f"Tour {tour + 1}",
                "started": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "matches": [],
                "description": self.Tournaments.description,
                "ended": None,
            }

            print(f"Pour le tour {tour + 1}")
            /print("tour + 1", tour + 1)
            self.tournament_view.display_first_turn()
            if tour + 1 == 1:
                matches = self.generate_random_match(tournaments_data.players)
                # Affichage des combinaisons de joueurs
                # print("Match :", matches)
                for match in matches:
                    print(f"{match[0].name} versus {match[1].name}")
                    # score1 = input if score1==1: score2==0 if score1==0.5: score2==0.5
                    # if score1==0: score2==1 else tournament view error
                    score1 = float(
                        input(colorise(f"Donner le score du joueur {match[0].name} : "))
                    )
                    # score2 = int(input(colorise(f"Donner le score du joueur {match[1].name} : ")))
                    if isinstance(score1, (int, float)):
                        if score1 == 1 or score1 == 0 or score1 == 0.5:
                            if score1 == 0.5:
                                score2 = score1
                            elif score1 == 1:
                                score2 = 0
                            else:
                                score1 = 0
                                score2 = 1

                        else:
                            print("Le score n'est pas valide.")
                    else:
                        print("Le score n'est pas un nombre.")

                    tour_obj["matches"].append(
                        ([match[0].player_uuid, score1], [match[1].player_uuid, score2])
                    )
                tournaments_data.turn_list.append(tour_obj)
                tournaments_data.turn = tour + 2
                # print("tour + 2", tour + 2)
                tournaments_data.ending_date = (datetime.now()).strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
                # print(tournaments_data.ending_date)
                tour_obj["ended"] = tournaments_data.ending_date
                tournaments_data.status = STATUS_PENDING
                tournaments_data.save_tournament()
                demande = input('"Q" pour clore le round: ').upper()
                if demande == "Q":
                    break
                # attention id tournament
            else:
                historique_matches = self.get_historique_matches(
                    tournaments_data.turn_list
                )
                # print("historique_matches", historique_matches)
                # for i in range(0, len(historique_matches)):
                #     historique_match = historique_matches[i]
                # print(historique_match)
                self.update_score_player(
                    tournaments_data.turn_list, tournaments_data.players
                )
                matches = self.generate_match(
                    tournaments_data.players, historique_matches
                )
                # print("Match :", matches)
                for match in matches:
                    print(f"{match[0].name} versus {match[1].name}")
                    # mettre plutot score1 = input if score1==1: score2==0 if score1==0.5: score2==05
                    # if score1==0: score2==1 else tournament view error
                    score1 = float(
                        input(colorise(f"Donner le score du joueur {match[0].name} : "))
                    )
                    # score2 = int(input(colorise(f"Donner le score du joueur {match[1].name} : ")))
                    if isinstance(score1, (int, float)):
                        if score1 not in [0, 0.5, 1]:
                            print("Score invalide. Svp entrer 0, 0.5, ou 1.")

                        if score1 == 0.5:
                            score2 = score1
                        elif score1 == 1:
                            score2 = 0
                        else:
                            score1 = 0
                            score2 = 1

                    else:
                        print("Le score n'est pas un nombre.")

                    tour_obj["matches"].append(
                        ([match[0].player_uuid, score1], [match[1].player_uuid, score2])
                    )
                tournaments_data.turn_list.append(tour_obj)
                tournaments_data.turn = tour + 1
                print("tour + 1 else ", tour + 1)
                # print(tournaments_data.status)
                tournaments_data.ending_date = (datetime.now()).strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
                tour_obj["ended"] = tournaments_data.ending_date
                tournaments_data.save_tournament()
                demande = input('"Q" pour clore le round: ').upper()
                if demande == "Q":
                    break
                if tour + 1 == tournaments_data.nb_turn:
                    self.tournament_view.get_comment()
                    tournaments_data.status = STATUS_END
                    break
                tournaments_data.save_tournament()
                # attention id tournament

    def generate_random_match(self, players):
        matches = []
        i = 0
        random.shuffle(players)
        while i < len(players):
            matches.append((players[i], players[i + 1]))
            # print(players[i], i)
            # print(players[i+1], i+1)
            i = i + 2
        return matches

    def generate_match(self, players, historique_matches):
        players_classes = sorted(players, key=lambda x: x.score)
        # print(players_classes)
        matches = []
        i = 0
        # algo pour que joueurs ne se rencontrent pas [(1,2),(3,4)]!=[(2,1),(4,5)]

        while i < len(players_classes):
            player_pairs = [
                players_classes[i].player_uuid,
                players_classes[i + 1].player_uuid,
            ]
            if player_pairs in historique_matches and i < len(players_classes) - 2:
                p = players_classes[i + 1]
                players_classes[i + 1] = players_classes[i + 2]
                players_classes[i + 2] = p

            matches.append((players_classes[i], players_classes[i + 1]))
            # print(players_classes[i], i)
            # print(players_classes[i+1], i+1)#
            i = i + 2

        # print(matches)

        return matches

    def get_historique_matches(self, turn_list):
        historique = []
        for tourn in turn_list:
            for match in tourn["matches"]:
                historique.append([match[0][0], match[1][0]])
                historique.append([match[1][0], match[0][0]])
        return historique

    def update_score_player(self, turn_list, players):
        for play in players:
            play.score = 0

            # parcoure tous les tours passes et rajoute score sur player.score
        for tourn in turn_list:
            for match in tourn["matches"]:
                # match[0][0] = id joueur_1, match[0][1] = score joueur_1
                # match[1][0] = id joueur_2, match[1][1] = score joueur_2
                found_player_1 = [p for p in players if p.player_uuid == match[0][0]][0]
                found_player_1.score = found_player_1.score + match[0][1]
                found_player_2 = [p for p in players if p.player_uuid == match[1][0]][0]
                found_player_2.score = found_player_2.score + match[1][1]
