def find_lines_starting_with(lines, key):
    return [m for m in lines if m.startswith(key)]


def print_list(list_to_print: list, end="\n"):
    for line in list_to_print:
        print(line, end=end)
