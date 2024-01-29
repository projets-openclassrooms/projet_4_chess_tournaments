from CONSTANTES import MIN_TURNS
from utils.settings import clear_screen, colorise, is_odd

"""Display Tournament view"""


# TOURNAMENT_NAME = r"^[A-Za-z0-9]{0,99}$"
# NB_TURN_FORMAT = r"^[0-9]{1,2}$"


class TournamentView:
    def __init__(self):
        self.demande = colorise(
            "\nChoix des joueurs :"
            + " Saisir l'identification du joueur ou "
            + " Utiliser les options suivantes : \n"
            + " 1 - Afficher la liste en cours d'entrée.\n"
            + " 2 - Sélectionner tous les joueurs.\n"
            + " 0 - pour revenir en arrière.\n"
        )

    def display_menu(self):
        menu = input(
            colorise(
                "Que souhaitez-vous faire ?\nSaisir le numéro :\n\n"
                + " 1 - Créer un nouveau tournoi? \n"
                + " 2 - Afficher les tournois? \n"
                + " 3 - Lancer un tournoi\n"
                + " 4 - Reprendre un tournoi en cours?\n"
                + " 0 - pour revenir en arrière.\n"
            )
        )
        clear_screen()
        return menu

    def display_first_turn(self) -> object:
        return (
            "Veuillez saisir le point du gagnant.\n"
            + "Le reste sera saisi automatiquement,\n"
            + "Gagnant : 1 , Perdant : 0, Egalité : 0.5\n"
        )

    def get_players(self):
        return (
            "Vous n'avez pas encore de joueur.\n"
            + "Avant de démarrer un tournoi,\n"
            + "Veuillez entrer des joueurs à enregistrer.\n"
        )

    def get_name(self) -> object:
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

    def get_location(self):
        location = ""

        while location == "":
            location = input(
                "Ou se passe ce tournoi? (Saisir '0' pour revenir au menu)\n"
            ).upper()
            if not location:
                print("Ce champ ne peut pas être vide")

        return location

    def get_description(self):
        description = ""

        while description == "":
            description = input("Description du tournoi?\n").upper()
            if not description:
                print("Ce champ ne peut pas être vide")

        return description

    def get_nb_turn(self):
        """
        turns isdigit() ok

        :rtype: object
        :return final_turn_nb
        """

        turns = input(
            "Combien de tours compte ce tournoi?\n-" + "par défaut (4 tours)\n"
        )
        if turns != int(MIN_TURNS):
            turns = int(MIN_TURNS)
        else:
            if not int(turns):
                self.display_error()

            else:
                turns = int(turns)
        return turns

    def list_players(self, player_list) -> object:
        """afficher liste de joueurs selectionnes

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
            print(colorise("\nListe des tournois enregistrés :\n"))
            print(
                "N° ",
                f"{'Nom':<16}{'- Statut ':<14} - {'Nombre joueurs':<20} - {'Nombre de tours':<12}\n",
            )
            i = 0
            for tournament in tournaments:
                i += 1
                if len(tournament.players) == 0:
                    return
                else:
                    print(
                        colorise(f"{i}-")
                        + f" {tournament.name:<16} -"
                        + colorise(f" {tournament.status:<12} -")
                        + f" {len(tournament.players)} joueurs inscrits."
                        + colorise(f" Nombre de tours : {tournament.nb_turn}")
                    )

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

    def display_saving_error(self):
        print("Le nom est déjà pris. Ressaisir un autre nom de tournoi svp.\n")

    def display_import_error(self):
        print("Problème pour importer le tournoi sélectionné.\n")

    def display_error(self):
        print("Erreur de saisie.")

    def get_comment(self):
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
