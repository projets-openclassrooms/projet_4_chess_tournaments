import random
from datetime import datetime

from CONSTANTES import COLOR, MAX_PLAYERS, STATUS_START, STATUS_PENDING, STATUS_ALL, STATUS_END
from model.match import Match
from model.player import Player
from model.tournament import Tournament
from model.turn import Turn
from view.matchview import MatchView
from view.playerview import PlayerView
from view.tournamentview import TournamentView
from view.turnview import TurnView

from utils.settings import clear_console, colorise, is_odd
from collections import Counter

"""Define controller about tournament
    choice of pairs
    create_tournament
    randomize for 1st turn
"""


# Constantes COLOR = ["Blanc", "Noir"]


class TournamentManager:
    """Define Tournament Manager"""

    def __init__(self):
        self.status = None
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.turn_view = TurnView()
        self.match_view = MatchView()
        self.tournament = None

    def create_tournament(self):
        """return self.tournament : New tournament with
        a name, a location, a list of players and
        a number of turns
        :param players_saved:
        :return: None"""
        # prompt user nom du tournoi, endroit, nombre de tours pour get liste des players
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

            if choix == "Q" or i == combien+1:
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
        print(f"{tournaments_data.nb_turn} tours pour ce tournoi.")
        # boucle tant que fin de saisie != Q
        clear_console()

        for tour in range(tournaments_data.nb_turn):
            tour_obj = {
                "name": f"Tour {tour + 1}",
                "started": str(datetime.now()),
                "matches": [],
            }

            print(f"Pour le tour {tour + 1}")
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
                tournaments_data.save_tournament()
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
                    # if score1==0: score2==1 else tournament view rror
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
                # print(tournaments_data.status)
                # print(type(tournaments_data.turn))
                # print(type(tournaments_data.nb_turn))
                if tournaments_data.turn == tournaments_data.nb_turn:
                    tournaments_data.status = STATUS_END
                    tournaments_data.status.replace(STATUS_PENDING, STATUS_END)
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

        while i < len(players_classes):
            player_pairs = [players_classes[i].player_uuid, players_classes[i + 1].player_uuid]
            if player_pairs in historique_matches and i < len(players_classes)-2:
                p = players_classes[i + 1]
                players_classes[i + 1] = players_classes[i + 2]
                players_classes[i + 2] = p

            matches.append((players_classes[i], players_classes[i + 1]))
            # print(players_classes[i], i)
            # print(players_classes[i+1], i+1)#
            i = i + 2

        # print(matches)
        # algo pour que joueurs ne se rencontrent pas [(1,2),(3,4)]!=[(2,1),(4,5)]

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
            turn_player_1 = turn_player_2 =[]

            # parcoure tous les tours passes et rajoute score sur player.score
        for tourn in turn_list:
            for match in tourn["matches"]:
                # match[0][0] = id joueur_1, match[0][1] = score joueur_1
                # match[1][0] = id joueur_2, match[1][1] = score joueur_2
                found_player_1 = [p for p in players if p.player_uuid == match[0][0]][0]
                found_player_1.score = found_player_1.score + match[0][1]
                found_player_2 = [p for p in players if p.player_uuid == match[1][0]][0]
                found_player_2.score = found_player_2.score + match[1][1]
                # print(found_player_2.score)
                # print(found_player_1.score)
                # turn_player_2.append((found_player_2.name,found_player_2.score))
                # turn_player_1.append((found_player_1.national_identification,found_player_1.score))
        # print(turn_player_1)
        # print(turn_player_2)
        # tourn['rankin'] = turn_player_2

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

        # Charger le tournoi spécifique

        tournament = Tournament.load_tournament_by_id(tournament_id)
        if not tournament:
            print(f"Tournament with ID {tournament_id} not found.")
            return
        player_points = {}
        new_tournament_score = 0
        score = 0
        for round_data in tournament.list_of_tours:
            for match_data in round_data.get("matches", []):
                for player_id, score in match_data:
                    player_points.setdefault(player_id, 0)
                    player_points[player_id] += score
                    # Mets à jour le score du tournoi dans le modèle Player

                    player = Player.get_player_by_id(player_id)
                    if player:
                        new_tournament_score = score
                        player.update_score_tournament(player_id, new_tournament_score)
                    else:
                        print(f"Joueur avec l'ID {player_id} non trouvé.")
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        print("Classement Final du Tournoi :\n")
        for player_id, points in sorted_players:
            player = Player.get_player_by_id(player_id)
            if player:
                print(f"{player.first_name} {player.last_name}: {points} points")
            else:
                print(f"Player with ID {player_id} not found.")
        print()
        return sorted_players

    def save_turn_data(self):
        """
        json dumps tournaments informations
        :rtype: object

        """
        new_turn = Turn.to_dict()

        if new_turn.start_round is None:
            new_turn.start_round = datetime.now()
            new_turn.update({"start": str(new_turn.start_round)})
        else:
            new_turn["start"] = str(new_turn.start_round)
        if new_turn.start_round:
            new_turn["end"] = str(new_turn.end_round)
        else:
            new_turn.update({"end": None})
        file_name = f"{file_tournament}.json"

        with open(file_name, "w") as file:
            json.dump(new_turn, file, default=lambda x: x.to_dict())

    def get_all_turn_files(self, t_name):
        """

        :param t_name:
        :return: file_list
        """
        turn_file = f"{REPORT_FILE}{t_name}_turn[0-9]{0, 99}.json$"
        file_list = []
        for root, _, files in os.walk(TOURNAMENT_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path.replace("\\", "/")
                if re.match(turn_file, file_path):
                    file_list.append(file_path)
        return file_list

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




