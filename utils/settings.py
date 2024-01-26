import datetime
from os import name, system


def clear_console():
    # for windows
    if name == "nt" or name == "win32":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def is_odd(length):
    return length % 2 != 0


def separation():
    print(colorise("#" * 30))


def when(predicate, when_true):
    return lambda x: when_true(x) if predicate(x) else x


class color:
    g = "\033[92m"  # vert
    y = "\033[93m"  # jaune
    r = "\033[91m"  # rouge
    n = "\033[0m"  # gris, couleur normale


def temps_formate(temps_json):
    date_time = datetime.datetime.strptime(temps_json, "%Y-%m-d %H:%M:%S.%f")
    date = date_time.date()
    heure = date_time.time()
    temps_formate = date.strftime("%d/%m/%Y") + " " + heure.strftime("%H:%M:%S")
    return temps_formate


def colorise(text):
    couleurs = [color.g, color.y, color.r]
    r = ""
    i = 0
    for c in text:
        if c.upper() == c:
            r += couleurs[i] + c + color.n
            i = (i + 1) % 3
        else:
            r += c

    return r
