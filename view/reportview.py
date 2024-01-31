from CONSTANTES import REPORT_FILE
from utils.settings import clear_screen, colorise

"""Define report views."""


class ReportView:
    """
    display_empty()
    display_import_error()
    ask_type_report()
    tournament_choice()
    display_create_report()
    display_create_error()
    open_error()

    """

    def display_empty(self):
        print("Vous n'avez aucune donnée enregistrée.\n")

    def display_import_error(self):
        print("Le tournoi saisi n'existe pas.\n")

    def get_type_report(self):
        """"""
        selection = int(
            input(
                colorise(
                    "Quel type de rapport aimeriez-vous afficher?\n"
                    + "- 1 Liste de tous les joueurs.\n"
                    + "- 2 Liste de tous les tournois.\n"
                    + "- 3 Noms et dates d'un tournoi donné.\n"
                    + "- 4 Liste de joueurs d'un tournoi.\n"
                    + "- 5 Détails des tours d'un tournoi et matchs.\n"
                    + "- 6 pour revenir en arrière.\n"
                )
            )
        )
        clear_screen()
        return selection

    def display_create_report(self):
        print("Le rapport a bien été créé.\n")
        print(f"Veuillez le trouver dans le dossier '{REPORT_FILE}'")
        clear_screen()

    def display_create_error(self):
        print("Le rapport n'a pas pu être créé.")

    def open_error(self):
        print("Le rapport n'a pas pu être trouvé.")
