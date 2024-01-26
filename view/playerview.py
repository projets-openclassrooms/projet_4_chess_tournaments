"""Define player view"""
import re

from CONSTANTES import BIRTHDAY_FORMAT, NATIONAL_IDENTIFICATION_FORMAT, QUIT
from utils.settings import clear_console, colorise, separation


class PlayerView:
    def display_menu(self):
        menu = input(
            colorise(
                "Quel menu souhaitez-vous sélectionner ?\nSaisir\n\n"
                + " 1 - Créer un nouveau joueur,\n"
                + " 2 - Voir les joueurs,\n"
                + " 0 - Menu précédent.\n"
            )
        )
        separation()
        input("Entrée pour continuer.")
        clear_console()
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
            print(colorise("\nListe des joueurs enregistrés :\n"))
            print("Numéro - (INE)    - Nom Prénom")
            i = 0
            for player in players_saved:
                i += 1
                print(
                    f"{i:<7}- {player.national_identification:<8} - {player.name} {player.firstname}"
                )
            if len(players_saved) == 1:
                print("1 Joueur.\nVeuillez saisir les données d'un autre joueur.\n")

            elif len(players_saved) > 1:
                print(f"Total : {str(len(players_saved))} joueurs.\n")
        separation()

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

    def get_name(self):
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

    def get_firstname(self):
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

    def get_birthdate(self):
        date_of_birth = ""
        while date_of_birth != QUIT:
            date_of_birth = input("Date de naissance (JJ/MM/AAAA): \n")
            if date_of_birth == "":
                print("Ce champ ne peut pas être vide")
            elif date_of_birth == QUIT:
                print("Vous quittez la création\n")
                return None
            elif re.match(BIRTHDAY_FORMAT, date_of_birth):
                return date_of_birth
            else:
                print("La date doit être au format '__/__/____'")

    def ask_national_identification(self):
        national_identification = ""
        while national_identification != QUIT:
            national_identification = input(
                "Identifiant national du joueur (AB12345) :\n"
            ).upper()
            if national_identification == "" or national_identification == "q":
                print("Vous quittez la création\n")
                return None
            elif re.match(NATIONAL_IDENTIFICATION_FORMAT, national_identification):
                return national_identification
            else:
                print("Le format attendu est 'AB12345'\n")

    def display_creation_error(self, national_identification):
        print(
            f"L'indentifiant '{national_identification} ' existe déjà dans la base de donnée.\n"
        )

    def display_creation(self):
        print("Le joueur à été créé")
