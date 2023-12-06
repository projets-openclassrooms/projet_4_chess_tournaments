"""
Constantes pour faire fonctionner l'application
"""
# Repertoires de data
DATA_FOLDER = "data/"
REPORT_FILE = "data/report/"
TOURNAMENT_FOLDER = "data/tournaments"
TOURNAMENT_FILES_NAME = r"^data/tournaments/[A-Za-z0-9]{0,99}.json$"

# liste des caractères autorisés
NATIONAL_IDENTIFIER_FORMAT = r"^[A-Z]{2}[0-9]{5}$"
BIRTHDAY_FORMAT = r"^[0-9]{1}[0-9]{1}/[0-9]{1}[0-9]{1}/[0-9]{4}$"
TOURNAMENT_NAME = r"^[A-Za-z0-9]{0,99}$"
NB_TURN_FORMAT = r"^[0-9]{1,2}$"
SEARCHING_INE = r"\((.*)\)"

# Constantes de jeu
MAX_PLAYERS = 8
MENU_JOUEURS = "1"
MENU_TOURNOI = "2"
MENU_GESTION = "3"
COLOR = ["Blanc", "Noir"]
QUIT = 4
