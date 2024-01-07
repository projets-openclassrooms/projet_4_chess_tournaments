from os import system, name
import datetime
def clear_console():
    # for windows
    if name == "nt" or name == "win32":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")

