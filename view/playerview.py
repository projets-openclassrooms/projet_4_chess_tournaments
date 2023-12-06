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
            print("\nAucun joueur choisi.\n")
        else:
            print("\nDétail de la liste des joueurs :\n")
            for player in players_saved:
                print(
                    f"- {player.name} {player.firstname} - {player.birthday}"
                    + f" - INE : {player.identifiant}"
                )
            if len(players_saved) == 1:
                print("Joueur n°1\n")
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

    def ask_for_name(self):
        name = ""
        while name != QUIT:
            name = input(
                "\nSaisissez le nom de famille du joueur ou 'q'"
                " pour quitter la création:\n> "
            ).upper()
            if name == "":
                print("Ce champ ne peut pas être vide")
            elif name == QUIT:
                print("Vous quittez la création\n")
                return None
            else:
                return name

    def ask_for_firstname(self):
        firstname = ""
        while firstname != QUIT:
            firstname = input(
                "Veuillez saisir le prénom du joueur "
                + " ou 'q' pour quitter la création :\n"
            ).upper()
            if firstname == "":
                print("Ce champ ne peut pas être vide")
            elif firstname == QUIT:
                print("Vous quittez la création\n")
                return None
            else:
                return firstname

    def ask_for_birthday(self):
        birthday = ""
        while birthday != QUIT:
            birthday = input(
                "Veuillez saisir la date de naissance du joueur.\n"
                + "Elle doit être au format"
                + " '__/__/____' "
                + ", mais vous pouvez quitter la création"
                + " à tout moment en tapant 'q':\n"
            ).upper()
            if birthday == "":
                print("Ce champ ne peut pas être vide")
            elif birthday == QUIT:
                print("Vous quittez la création\n")
                return None
            elif re.match(BIRTHDAY_FORMAT, birthday):
                return birthday
            else:
                print(+"La date doit être au format" + " '__/__/____'")

    def ask_national_identification(self):
        identifiant = ""
        while identifiant != QUIT:
            identifiant = input(
                "Veuillez saisir l'identifiant national du joueur.\n"
                + "Il doit être au format"
                + " 'AB12345'"
                + ", mais vous pouvez également quitter"
                + " la création en tapant 'q'.\n"
            ).upper()
            if identifiant == "":
                print("Vous quittez la création\n")
            elif identifiant == QUIT:
                print("Vous quittez la création\n")
                return None
            elif re.match(NATIONAL_IDENTIFIER_FORMAT, identifiant):
                return identifiant
            else:
                print("Le format attendu est" + " 'AB12345'\n")

    def display_creation_error(self, identifiant):
        print(
            "L'indentifiant '" + identifiant + "' existe déjà dans la base de donnée.\n"
        )

    def display_creation(self):
        print("Le joueur à été créé")
