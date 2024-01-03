"""Define player view"""
import re
from CONSTANTES import QUIT, BIRTHDAY_FORMAT, NATIONAL_IDENTIFIER_FORMAT


class PlayerView:
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
                print("1 Joueur.\nVeuillez saisir les données d'un autre joueur\n")

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

    def delete_player(self, players_saved):
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

    def ask_for_name(self):
        name = ""
        while name != QUIT:
            name = input("\nSaisissez le nom de famille du joueur ").upper()
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
            firstname = input("Veuillez saisir le prénom du joueur ").upper()
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
            birthday = input(
                "Veuillez saisir la date de naissance du joueur.\n"
                + "Elle doit être au format '__/__/____' \n"
            ).upper()
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
            identifier = input(
                "Veuillez saisir l'identifier national du joueur.\n"
                + "Il doit être au format 'AB12345'"
                + ", mais vous pouvez également quitter"
                + " la création en tapant 'q'.\n"
            ).upper()
            if identifier == "" or identifier == "q":
                print("Vous quittez la création\n")
                return None
            elif re.match(NATIONAL_IDENTIFIER_FORMAT, identifier):
                return identifier
            else:
                print("Le format attendu est 'AB12345'\n")

    def display_creation_error(self, identifier):
        print(f"L'indentifiant '{identifier} ' existe déjà dans la base de donnée.\n")

    def display_creation(self):
        print("Le joueur à été créé")
