from collections.abc import Sequence


def find_lines_starting_with(lines: Sequence[str], key: str) -> Sequence[str]:
    return [m for m in lines if m.startswith(key)]


def print_list(list_to_print: Sequence, end: str = "\n"):
    for line in list_to_print:
        print(line, end=end)
