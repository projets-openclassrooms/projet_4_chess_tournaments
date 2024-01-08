import os
import datetime

# import only system from os

"""
Constantes pour faire fonctionner l'application
"""
# Repertoires de data
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = r"data/"
# f"{ABSOLUTE_PATH}data/"
file_tournament = f"{DATA_FOLDER}tournaments.json"
file_players = f"{DATA_FOLDER}players.json"
REPORT_FILE = f"{DATA_FOLDER}report/"
TOURNAMENT_FOLDER = f"{DATA_FOLDER}"
# TOURNAMENT_FILES_NAME = r"^data/tournaments/[A-Za-z0-9]{0,99}.json$"

# liste des caractères autorisés
NATIONAL_IDENTIFIER_FORMAT = r"^[A-Z]{2}[0-9]{5}$"
BIRTHDAY_FORMAT = r"^[0-9]{1}[0-9]{1}/[0-9]{1}[0-9]{1}/[0-9]{4}$"
TOURNAMENT_NAME = r"^[A-Za-z0-9]{0,99}$"
NB_TURN_FORMAT = r"^[0-9]{1,2}$"
SEARCHING_INE = r"\((.*)\)"

# Constantes de jeu
MIN_TURNS = 4
MAX_PLAYERS = 8
MENU_JOUEURS = "1"
MENU_TOURNOI = "2"
MENU_GESTION = "3"
COLOR = ["Blanc", "Noir"]
QUIT = "Q"


def birth_format(d):
    try:
        d = datetime.datetime.strptime(d, "%dd/%mm/%YYYY")
    except:
        return f"erreur de date : {d} n'est pas valable."
