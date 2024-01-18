from os import system, name
import datetime
import uuid

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


lipsum = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut purus elit, vestibulum ut, placerat ac, adipiscing vitae, felis. Curabitur dictum gravida mauris. Nam arcu libero, nonummy eget, consectetuer id, vulputate a, magna. Donec vehicula augue eu neque. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Mauris ut leo. Cras viverra metus rhoncus sem. Nulla et lectus vestibulum urna fringilla ultrices. Phasellus eu tellus sit amet tortor gravida placerat. Integer sapien est, iaculis in, pretium quis, viverra ac, nunc. Praesent eget sem vel leo ultrices bibendum. Aenean faucibus. Morbi dolor nulla, malesuada eu, pulvinar at, mollis ac, nulla. Curabitur auctor semper nulla. Donec varius orci eget risus. Duis nibh mi, congue eu, accumsan eleifend, sagittis quis, diam. Duis eget orci sit amet orci dignissim rutrum."


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


# print(colorise(lipsum))

myuuid = uuid.uuid4()
myuuidStr = str(myuuid)

sameMyUuid = uuid.UUID(myuuidStr)
assert myuuid == sameMyUuid

# print(myuuid, myuuidStr, sameMyUuid
#       )