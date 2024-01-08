"""Define player view"""
import re
from CONSTANTES import QUIT, BIRTHDAY_FORMAT, NATIONAL_IDENTIFIER_FORMAT


class PlayerView:
    def display_menu(self):
        menu = input(
            "Quel menu souhaitez-vous sélectionner ?\nTaper\n\n"
            + " 1 - Créer un nouveau joueur \n"
            + " 2- Voir les joueurs\n"
            + " 0 - quitter.\n"
        )
        # + " 2 - Supprimer un joueur\n"
        # + " 3 - Modifier un joueur\n"
        return menu

    def display_all_player_saved(self, players_saved):
        """
        display player's info saved

        :param players_saved:
        """
        if len(players_saved) == 0:
            print("\nAucun joueur choisi. probleme dans le fichier\n")
        else:
            print("\nListe des joueurs enregistrés :\n")
            i = 0
            for player in players_saved:
                i += 1
                print(
                    f"{i}- {player.name} {player.firstname} - {player.date_of_birth}"
                    + f" - INE : {player.identifier}"
                )
            if len(players_saved) == 1:
                print("1 Joueur.\nVeuillez saisir les données d'un autre joueur.\n")

            elif len(players_saved) > 1:
                print(f"Total : {str(len(players_saved))} joueurs.\n")

    def add_again(self):
        again = ""
        while again != "N" or again != "O":
            save_new_player = input(
                "Souhaitez-vous ajouter un nouveau joueur?(o/n)\n"
            ).upper()
            if save_new_player == "O":
                return True
            elif save_new_player == "N":
                return False
            else:
                print(f"{save_new_player} n'est pas valide\n")

    def ask_to_delete_player(self, players_saved):
        i = 0
        for player in players_saved:
            i += 1
            print(f"{i} - {player}")
            while True:
                choice = int(input("Saisir le numéro du joueur à supprimer :\n"))
                if not choice:
                    print("Merci de saisir un chiffre svp.")
                else:
                    return players_saved[choice - 1]

    def ask_to_modify_player(self, players_saved):
        i = 0
        for player in players_saved:
            i += 1
            print(f"{i} - {player}")
            while True:
                choice = int(input("Saisir le numéro du joueur à modifier :\n"))
                if not choice:
                    print("Merci de saisir un chiffre svp.")
                else:
                    return players_saved[choice - 1]

    def ask_for_name(self):
        name = ""
        while name != QUIT:
            name = input("\nSaisissez le nom de famille du joueur ").capitalize()
            if name == "":
                print("Ce champ ne peut pas être vide")
            elif name == "Q":
                print("Vous quittez la création\n")
                return None
            else:
                return name

    def ask_for_firstname(self):
        firstname = ""
        while firstname != QUIT or firstname != "q":
            firstname = input("Veuillez saisir le prénom du joueur ").capitalize()
            if firstname == "":
                print("Ce champ ne peut pas être vide")
            elif firstname == "Q":
                print("Vous quittez la création\n")
                return None
            else:
                return firstname

    def ask_for_birthday(self):
        birthday = ""
        while birthday != QUIT:
            birthday = input("Date de naissance (JJ/MM/AAAA): \n")
            if birthday == "":
                print("Ce champ ne peut pas être vide")
            elif birthday == QUIT:
                print("Vous quittez la création\n")
                return None
            elif re.match(BIRTHDAY_FORMAT, birthday):
                return birthday
            else:
                print("La date doit être au format '__/__/____'")

    def ask_national_identification(self):
        identifier = ""
        while identifier != QUIT:
            identifier = input("Identifiant national du joueur (AB12345) :\n").upper()
            if identifier == "" or identifier == "q":
                print("Vous quittez la création\n")
                return None
            elif re.match(NATIONAL_IDENTIFIER_FORMAT, identifier):
                return identifier
            else:
                print("Le format attendu est 'AB12345'\n")

    def select_player(self, players):
        """
        Permet à l'utilisateur de sélectionner un joueur parmi une liste de joueurs.

        Args:
            players (list): Liste des joueurs.

        Returns:
            int: L'indice du joueur sélectionné dans la liste.
        """
        print("\nSélectionnez un joueur : ")
        players_reversed = list(reversed(players))
        print(players_reversed)
        for i, player in enumerate(players_reversed):
            print(
                f"{i + 1} - "
                f"{player['nom']} "
                f"{player['prenom']} - "
                f"Né le {player['birthday']} - "
                f"ID: {player['national_identification']}"
            )

        while True:
            try:
                player_index = (
                    int(
                        input(
                            "\nEntrez le numéro du joueur que vous voulez sélectionner : "
                        )
                    )
                    - 1
                )
                if player_index < 0 or player_index >= len(players_reversed):
                    print(
                        "Numéro de joueur invalide. Veuillez entrer un numéro de joueur valide."
                    )
                else:
                    return len(players) - 1 - player_index
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")

    def display_creation_error(self, identifier):
        print(f"L'indentifiant '{identifier} ' existe déjà dans la base de donnée.\n")

    def display_creation(self):
        print("Le joueur à été créé")
