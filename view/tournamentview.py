import re
from time import sleep


from CONSTANTES import TOURNAMENT_NAME, NB_TURN_FORMAT, MIN_TURNS
from model.player import Player

from utils.settings import clear_console, is_odd

"""Display Tournament view"""
# TOURNAMENT_NAME = r"^[A-Za-z0-9]{0,99}$"
# NB_TURN_FORMAT = r"^[0-9]{1,2}$"


class TournamentView:
    def __init__(self):
        self.demande = (
            "\nChoix des joueurs :"
            + " taper l'identification du joueur ou "
            + " utiliser les options suivantes : \n"
            + " 1 - Afficher la liste en cours d'entrée.\n"
            + " 2 - Sélectionner tous les joueurs.\n"
            + " 0 - Menu précédent.\n"
        )

    def display_menu(self):
        menu = input(
            "Que souhaitez-vous sélectionner ?\nTaper\n\n"
            + " 1 - Voulez-vous créer un nouveau tournoi? \n"
            + " 2 - Voulez-vous afficher les tournois? \n"
            + " 3 - lancer un tournoi\n"
            + " 4 - reprendre un tournoi en cours?\n"
            + " 0 - menu précédent.\n"
        )
        clear_console()
        return menu

    def display_first_turn(self):
        return (
            "Vous n'avez pas encore de tournoi.\n"
            + "Avant de commencer un tournoi,\n"
            + "Veuillez entrer les informations du tournoi.\n"
        )

    def ask_for_players(self):
        return (
            "Vous n'avez pas encore de joueur.\n"
            + "Avant de démarrer un tournoi,\n"
            + "Veuillez entrer des joueurs à enregistrer.\n"
        )

    def ask_for_name(self) -> object:
        """

        :rtype: object
        :return name
        """

        name = ""
        while name == "":
            name = input("Quel est le nom de ce tournoi?\n").upper()

            if not name:
                print("Ce champ ne peut pas être vide")
        return name

    def ask_for_location(self):
        location = ""

        while location == "":
            location = input(
                "Ou se passe ce tournoi? (tapez '0' pour revenir au menu)\n"
            ).upper()
            if not location:
                print("Ce champ ne peut pas être vide")

        return location

    def ask_for_description(self):
        description = ""

        while description == "":
            description = input("Description du tournoi?\n").upper()
            if not description:
                print("Ce champ ne peut pas être vide")

        return description

    def ask_for_nb_turn(self):
        """
        turns isdigit() ok

        :rtype: object
        :return final_turn_nb
        """

        turns = input(
            "Combien de tours compte ce tournoi?\n-" + "par défaut (4 tours)\n"
        )
        if not turns:
            turns = MIN_TURNS
        else:
            if not int(turns):
                self.display_error()

            else:
                turns = int(turns)
        return turns

    def list_players(self, player_list) -> object:
        """ afficher liste de joueurs selectionnes

        :rtype: object a
        :return len(player_list)
        """
        if not player_list:
            print("Votre liste de joueurs sélectionnés est vide.")
        elif len(player_list) == 1:
            print("Ajouter d'autres joueurs svp., 1 joueur saisi")
        elif len(player_list) > 1:
            print(f"Votre liste de joueurs sélectionnés: {len(player_list)} joueurs")
        return player_list

    def display_all_tournaments(self, tournaments):
        """
        display tournaments info saved

        :param tournaments:
        """
        if len(tournaments) == 0:
            print("\nAucun tournoi\n")
        else:
            print("\nListe des tournois enregistrés :\n")
            i = 0
            for tournament in tournaments:
                i += 1
                print(f"{i}- {tournament.name}")

        clear_console()

    def display_tournament_players(self, players_saved):
        """

        :param players_saved:
        :return"{id} {player}"

        """
        print("Les joueurs déjà enregistrés sont: ")
        index = 1
        for player in players_saved:
            print(f"{index}-{str(player)}")
            index += 1

    def display_current_list(self, current_list):
        """

        :param current_list:
        :return str (len(current_list)) + " joueur(s)
        """
        print("La liste en cours d'entrée actuelle est :")
        if not current_list:
            print("Votre liste est vide")
        else:
            print("Votre liste actuelle: ")
            for player in current_list:
                print(player)
            print("Pour un total de: " + str(len(current_list)) + " joueur(s)\n")

    def incomplete_list(self, current_list):
        print(f"\n{current_list} joueurs inscrits.")
        if is_odd(current_list) and current_list < 8:
            print("votre liste n'est pas paire ou incomplète.\nA compléter svp.\n")

    def quit_select_current(self, current_list):
        """

        :param current_list:
        """
        if current_list:
            print("Votre liste est actuellement constituée de: ")
            for player in current_list:
                print(player)
            print(f"\nsur: {len(current_list)} joueurs.")
            if len(current_list) % 2 != 0:
                print("Votre liste n'est pas paire, veuillez reprendre\n")
        else:
            print("Votre liste est vide, elle ne peut pas être vide")

    def select_players(self, players_saved):
        """

        :param players_saved:
        :return: player_list or None
        """
        player_list = []
        decision = False
        while not decision:
            self.list_players(player_list)
            self.display_tournament_players(players_saved)
            current_player = input(self.demande)
            if current_player == "":
                print("Ce champ ne peut pas être vide")
            elif current_player == "1":
                self.display_current_list(player_list)
                continue
            elif current_player == "2":
                player_list = players_saved
                if len(player_list) % 2 != 0:
                    print("La liste de tous les joueurs n'est pas paire.\n")
                else:
                    return player_list
            # elif current_player == "3":
            #     self.quit_select_current(player_list)
            #     return player_list
            elif current_player == "Q":
                return None
            elif current_player in player_list:
                print(f"{current_player} est déjà dans la liste")
            else:
                player_exist = False
                for player in player_list:
                    if current_player in player.national_identification:
                        print("Le joueur est déjà enregistré.\n")
                        player_exist = True
                        break
                if player_exist:
                    continue
                for player in players_saved:
                    if current_player == player.national_identification:
                        player_list.append(player)
                        break

    def ask_to_continue(self):
        """

        :return: 1/2/0
        """
        while True:
            ask_to_new = input(
                "(1) - Nouveau tournoi,\n"
                + "(2) - Reprendre un tournoi en cours\n"
                + "'1' '2' ou '0' pour quitter?\n"
            )
            if ask_to_new == "1":
                return True
            elif ask_to_new == "2":
                return False
            elif ask_to_new == "0":
                return None
            else:
                print(f"{ask_to_new} n'est pas valide")

    def display_saving_error(self):
        print("Le nom est déjà pris. Ressaisir un autre nom de tournoi svp.\n")

    def display_import_error(self):
        print("Problème pour importer le tournoi sélectionné.\n")

    def display_error(self):
        return f"Erreur de saisie."

    def ask_to_comment(self):
        """

        :return: comment or None
        """
        comment_confirm = ""
        while comment_confirm != "O" or comment_confirm != "N":
            comment = input(
                "Le tournoi étant terminé, avez-vous un commentaire" + " à saisir?\n"
            ).upper()
            if comment:
                comment_confirm = input(
                    "Voulez-vous laisser ce commentaire ?"
                    + f" \n'{comment}'"
                    + "\n(o/n)"
                ).upper()
                if comment_confirm == "O":
                    return comment
            elif not comment:
                return None
