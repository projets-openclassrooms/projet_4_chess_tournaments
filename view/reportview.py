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
        print("Vous n'avez aucune donnée enregistrée.")

    def display_import_error(self):
        print("Le tournoi saisi n'existe pas.\n")

    def ask_type_report(self):
        """
        end_selection report's choice view

        :return: selection joueurs, tournois, matchs, quitter le programme
        """
        end_selection = False
        while not end_selection:
            selection = input(
                "\nQuel type de rapport aimeriez-vous créer?\n"
                + "-Tous les joueurs.(1)\n"
                + "-Tous les tournois.(2)\n"
                + "-Tous les matchs d'un tournoi.(3)\n"
                + "-Tous les joueurs d'un tournoi (4).\n"
                + "-Ou tapez 'q' pour quitter.\n"
            ).upper()
            if selection in range(1, 5, 1):
                return selection
            elif selection == "Q":
                print("\nVous quittez maintenant la gestion de rapport.")
                return None
            else:
                print(selection + " n'est pas valide")

    def tournament_choice(self, all_tournaments):
        """

        :param all_tournaments:
        :return: choice
        """
        print("Voici les tournois sauvegardés: ")
        for tournament in all_tournaments:
            print("--> " + tournament)
        choice = input(
            "Taper le nom du tournoi dont vous souhaitez le rapport"
            + " ou tapez 'q' pour quitter.\n> "
        ).upper()
        if choice == "Q":
            return None
        return choice

    def display_create_report(self):
        print("Le rapport a bien été créé.")

    def display_create_error(self):
        print("Le rapport n'a pas pu être créé.")

    def ask_to_open(self):
        """

        :return: boolean
        """
        asking = True
        while asking:
            to_open = input(
                "\nSouhaitez-vous visualiser le " + "contenu de ce rapport? (o/n)\n> "
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
