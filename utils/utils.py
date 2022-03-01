def findLinesStartingWith(lines, key):
    return [m for m in lines if m.startswith(key)]


def printList(list, end="\n"):
    for line in list:
        print(line, end=end)