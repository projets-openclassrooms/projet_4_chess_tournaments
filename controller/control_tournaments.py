import random
from datetime import datetime

from CONSTANTES import COLOR, MAX_PLAYERS, STATUS_START, STATUS_PENDING, STATUS_ALL
from model.match import Match
from model.player import Player
from model.tournament import Tournament
from model.turn import Turn
from view.matchview import MatchView
from view.playerview import PlayerView
from view.tournamentview import TournamentView
from view.turnview import TurnView

from utils.settings import clear_console, colorise, is_odd

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
        name = self.tournament_view.ask_for_name()
        location = self.tournament_view.ask_for_location()
        description = self.tournament_view.ask_for_description()
        nb_turn = self.tournament_view.ask_for_nb_turn()
        players_saved = Player.get_players_saved()
        self.player_view.display_all_player_saved(players_saved)
        choix = ""

        # initialise liste players du tournoi depuis players_saved
        players = []
        nb_players = len(players_saved)
        # loop pour atteindre 8 players max ou Q pour quitter
        while choix!="Q":
            if len(players) < MAX_PLAYERS and len(players) % 2 != 0:
                for player in players:
                    print(player)
            choix = input(
                    "Ajouter un joueur en indiquant son numéro ou Q pour quitter?"
                ).upper()

            if choix == "Q":
                break
            try:

                index = int(choix) - 1
                if 0 <= index < nb_players and players_saved[index] not in players:
                    players.append(players_saved[index])
                elif is_odd(players):
                    self.tournament_view.incomplete_list(players)
                else:
                    print("Veuillez entre un numéro valide")
            except ValueError:
                print("Veuillez entre un numéro valide")
        # while choix != "Q":
        #     choix = input(
        #         "Ajouter un joueur en indiquant son numéro ou Q pour quitter?"
        #     ).upper()
        #
        #     if choix == "Q":
        #         break
        #     # verifier que index = choix (choix - 1 pour avoir index)
        #
        #     index = int(choix) - 1
        #     if 0 <= index < nb_players and players_saved[index] not in players:
        #         players.append(players_saved[index])
        #     elif is_odd(players):
        #         self.tournament_view.incomplete_list(players)
        #     else:
        #         print("Veuillez entre un numéro valide")
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
                # print(f"tournoi sélectionné : {tournament.name}, {tournament.players}")
                # si aucun tournoi donc break
                if not tournament_to_choose:
                    print(colorise("Pas de tournoi."))
                print(f"tournoi sélectionné : {tournament_to_choose.name}")
                self.start_tournament(tournament_to_choose)

            elif menu == "4":
                # rappeler un tournoi
                tournament_to_choose = self.select_tournament(status=STATUS_PENDING)
                self.resume_tournament(tournament_to_choose)

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
        else:
            filtered_tournaments = [
                tournament_to_choose
                for tournament_to_choose in tournaments_data
                if tournament_to_choose.status == STATUS_PENDING
            ]

        self.tournament_view.display_all_tournaments(filtered_tournaments)

        while True:
            choix = input("Choisir le tournoi ou Q pour quitter? ").upper()
            if choix == "Q":
                break
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

        return tournament_to_choose

    def start_tournament(self, tournaments_data):
        # recuperer fromdict tournament
        # recuperer fromdict players
        # recuperer la liste des players  du tournoi

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

        for tour in range(tournaments_data.nb_turn):
            tour_obj = {
                "name": f"Tour {tour + 1}",
                "started": str(datetime.now()),
                "matches": [],
            }

            print(f"Pour le tour {tour + 1}")
            if tour + 1 == 1:
                matchs = self.generate_random_match(tournaments_data.players)
                # Affichage des combinaisons de joueurs
                print("Match :", matchs)
                for match in matchs:
                    print(f"{match[0].name} versus {match[1].name}")
                    # mettre plutot score1 = input if score1==1: score2==0 if score1==0.5: score2==05
                    # if score1==0: score2==1 else tournament view rror
                    score1 = float(input(colorise(f"Donner le score du joueur {match[0].name} : ")))
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
                print("historique_matches", historique_matches)
                self.update_score_player(
                    tournaments_data.turn_list, tournaments_data.players
                )
                matchs = self.generate_match(
                    tournaments_data.players, historique_matches
                )
                print("Match :", matchs)
                for match in matchs:
                    print(f"{match[0].name} versus {match[1].name}")
                    # mettre plutot score1 = input if score1==1: score2==0 if score1==0.5: score2==05
                    # if score1==0: score2==1 else tournament view rror
                    score1 = float(input(colorise(f"Donner le score du joueur {match[0].name} : ")))
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
                tournaments_data.turn = tour + 1
                tournaments_data.save_tournament()
                # attention id tournament

    def resume_tournament(self, tournament):
        print(f"Résumé du tournoi {tournament.name}")
        # affichage liste des joueurs tournoi

        # input saisie des scores
        # (joueur,scores) = input()
        # demander si saisie terminee
        # enregistrer resultat par serialisation

    def generate_random_match(self, players):
        matchs = []
        i = 0
        random.shuffle(players)
        while i < len(players):
            matchs.append((players[i], players[i + 1]))
            i = i + 2
        return matchs

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

    def restore_turn(self, turn_to_restore):
        """

        :param turn_to_restore:
        :return: turn_to_return
        """
        path_control = os.path.exists(turn_to_restore)
        if path_control is True:
            with open(turn_to_restore, "r") as file:
                all_infos = json.load(file)
            t_name = all_infos["tournament_name"]
            turn_nb = all_infos["turn_nb"]
            match_list = all_infos["match_list"]
            turn_to_return = cls(t_name, turn_nb, match_list)
            turn_to_return.starting_turn = all_infos["start"]
            if all_infos["end"]:
                turn_to_return.ending_turn = all_infos["end"]
        else:
            turn_to_return = None
        return turn_to_return

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

    def get_historique_matches(self, turn_list):
        historique = []
        for tourn in turn_list:
            for match in tourn["matches"]:
                historique.append([match[0][0], match[1][0]])
                historique.append([match[1][0], match[0][0]])

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

    def generate_match(self, players, historique_matches):
        players_classes = sorted(players, key=lambda x: x.score)
        matchs = []
        i = 0
        while i < len(players_classes):
            matchs.append((players_classes[i], players_classes[i + 1]))
            #
            i = i + 2
        # algo pour que joueurs ne se rencontrent pas [(1,2),(3,4)]!=[(2,1),(4,5)]

        return matchs
