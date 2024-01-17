from utils.settings import colorise

REPORT_FILE = "data/report/"

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
        print("Veuillez retourner dans le menu correspondant svp.")

    def display_import_error(self):
        print("Le tournoi saisi n'existe pas.\n")

    def ask_type_report(self):
        """
        end_selection report's choice view

        :return: selection joueurs, tournois, matchs, quitter le programme
        """
        end_selection = False
        while not end_selection:
            selection = int(
                input(colorise(
                    "Quel type de rapport aimeriez-vous créer?\n"
                    + "- 1 Tous les joueurs.\n"
                    + "- 2 Tous les tournois.\n"
                    + "- 3 Tous les résultats de matchs de tournoi(s).\n"
                    + "- 4 Tous les joueurs participant au(x) tournoi(s).\n"
                    + "- 5 pour revenir en arrière.\n"
                ))
            )

            if selection in range(1, 5, 1):
                return selection
            elif selection == 5:
                print("\nVous quittez maintenant la gestion de rapport.")
                return selection
            else:
                print(f"{selection} n'est pas valide")

    def tournament_choice(self, all_tournaments):
        """

        :param all_tournaments:
        :return: choice
        """
        i = 0
        print("Voici les tournois sauvegardés: ")
        for tournament in all_tournaments:
            i = i + 1
            print(f"{i}-->  {tournament}")

        choice = int(
            input(
                "Saisir le nom du tournoi dont vous souhaitez le rapport"
                + " ou Saisir 0 pour revenir en arrière.\n> "
            )
        )
        choice_tournament = all_tournaments[choice - 1]

        return choice_tournament

    def display_create_report(self):
        print("Le rapport a bien été créé.\n")
        print(f"Veuillez le trouver dans le dossier '{REPORT_FILE}'")

    def display_create_error(self):
        print("Le rapport n'a pas pu être créé.")

    def ask_to_open(self):
        """

        :return: boolean
        """
        asking = True
        while asking:
            to_open = input(
                "\nSouhaitez-vous visualiser le " + "contenu de ce rapport? (o/n)\n "
            ).upper()
            if to_open == "O":
                return True
            elif to_open == "N":
                return False
            else:
                print(to_open + " n'est pas valide.\n")

    def open_error(self):
        print("Le rapport n'a pas pu être trouvé.")

    def display_content(self, line_to_visualized):
        for element in line_to_visualized:
            print(element.replace(";", ", "))
