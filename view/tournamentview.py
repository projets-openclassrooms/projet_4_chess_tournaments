import re
from CONSTANTES import TOURNAMENT_NAME, NB_TURN_FORMAT
from model.player import Player

"""Display Tournament view"""
# TOURNAMENT_NAME = r"^[A-Za-z0-9]{0,99}$"
# NB_TURN_FORMAT = r"^[0-9]{1,2}$"


class TournamentView:
    def __init__(self):
        self.demande = (
            "\nChoix des joueurs :"
            + " taper l'identification du joueur ou "
            + " utiliser les options suivantes : \n"
            + " -Taper 1 pour afficher la liste en cours d'entrée.\n"
            + " -Taper 2 pour sélectionner tous les joueurs.\n"
            + " -Taper '0' pour quitter la création.\n"
        )
        
    def display_menu(self):
        
        menu = input(
            "Quel menu souhaitez-vous sélectionner ?\nTaper\n\n"
            + " 1 - Voulez-vous créer un nouveau tournoi? \n"
            + " 2 - reprendre un tournoi en cours?\n"
            + " 0 - quitter.\n"
        )
        return menu
    def ask_for_players(self):
        return (
            "Vous n'avez pas encore de joueur.\n"
            + "Avant de démarrer un tournoi,\n"
            + "Veuillez entrer des joueurs à enregistrer.\n"
        )

    def ask_for_name(self, all_existing_tournament) -> object:
        """

        :rtype: object
        :return name
        """
        name_confirmation = ""
        name = ""
        while name_confirmation != "O" or name != "Q":
            if not all_existing_tournament:
                print("Vous n'avez pas encore enregistré de tournoi\n")
            else:
                print("Voici les noms de tournoi déjà créés:\n")
                for tournament in all_existing_tournament:
                    print(tournament)
            name = input(
                "Quel est le nom de ce tournoi?" + " ('0' pour revenir au menu)\n"
            ).upper()
            name = name.replace(" ", "")
            if not name:
                print("Ce champ ne peut pas être vide")
            elif re.match(TOURNAMENT_NAME, name):
                if name == "0":
                    return None
                else:
                    return name

    def ask_for_location(self):
        location_confirmation = ""
        location = ""

        while location_confirmation != "O" or location != "Q":
            location = input(
                "Ou se passe ce tournoi? (tapez '0' pour revenir au menu)\n"
            ).upper()
            if not location:
                print("Ce champ ne peut pas être vide")
            elif location == "0":
                return None
            else:
                return location

    def ask_for_nb_turn(self, players):
        """

        :rtype: object
        :return final_turn_nb
        """
        perfect_choice = int(len(players) / 2)
        perfect_choice = perfect_choice * 2
        valide_confirmation = ""
        turns = ""
        final_turn_nb = 0
        while valide_confirmation != "O" or turns != "Q":
            turns = input(
                "Combien de tours compte ce tournoi?\n-"
                + "par défaut (4 tours)"
                + f" ({perfect_choice} joueurs jouent).\n"
                + " et tapez '0' pour quitter,\n"
            ).upper()
            if not turns:
                print("Ce champ ne peut pas être vide")
            elif turns == "4":
                final_turn_nb = 4
                return final_turn_nb
            elif turns == "0":
                return None
            elif re.match(NB_TURN_FORMAT, turns):
                try:
                    final_turn_nb = int(turns)
                except ValueError:
                    print(f"'{final_turn_nb}' n'est pas valide")
            else:
                return final_turn_nb

    def list_players(self, player_list) -> object:
        """

        :rtype: object
        :return len(player_list)
        """
        if not player_list:
            print("Votre liste de joueurs sélectionnés est vide.")
        elif len(player_list) == 1:
            print("Votre liste comporte 1 joueur.")
            +print("Ajouter d'autres joueurs svp.")
        elif len(player_list) > 1:
            print(f"Votre liste de joueurs sélectionnés: {len(player_list)} joueurs")

    def display_tournament_players(self, players_saved):
        """

        :param players_saved:
        :return"{player.name} {player.firstname}"
                + f", né le {player.birthday} et son identifier: {player.identifier}"
        """
        print("Les joueurs déjà enregistrés sont: ")
        index = 1
        for player in players_saved:
            print(f"{index}-{str(player)}")
            index += 1

    def display_current_list(self, current_list):
        """

        :param current_list:
        :return str(len(current_list)) + " joueur(s)
        """
        print("La liste en cours d'entrée actuelle est :")
        if not current_list:
            print("Votre liste est vide")
        else:
            print("Votre liste actuelle: ")
            for player in current_list:
                print(player)
            print("Pour un total de: " + str(len(current_list)) + " joueur(s)\n")

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
                    if current_player in player.identifier:
                        print("Le joueur est déjà enregistré.\n")
                        player_exist = True
                        break
                if player_exist:
                    continue
                for player in players_saved:
                    if current_player == player.identifier:
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

    def select_previous_tournament(self, tournament_saved):
        """

        :param tournament_saved:
        :return: selected or None
        """
        if not tournament_saved:
            print("Il n'y a aucun tournoi commencé ou sauvegardé.\n")
            return None
        selected = ""
        while selected not in tournament_saved:
            print("Voici la liste de tous les tournois précédents :")
            for tournament in tournament_saved:
                print("--" + tournament)
            selected = input("Tapez le nom d'un tournoi ou '0' pour quitter.\n").upper()
            if selected in tournament_saved:
                return selected
            elif selected == "0":
                return None
            else:
                print(selected + " n'est pas valide")

    def display_saving_error(self):
        print("Le nom est déjà pris. Ressaisir un autre nom de tournoi svp.\n")

    def display_import_error(self):
        print("Problème pour importer le tournoi sélectionné.\n")

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
