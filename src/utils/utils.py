from collections.abc import Sequence


def find_lines_starting_with(lines: Sequence[str], key: str) -> Sequence[str]:
    return [m for m in lines if m.startswith(key)]


def find_first_line_starting_with(lines: Sequence[str], key: str) -> str:
    for line in lines:
        if line.startswith(key):
            return line
    return ""


def print_list(list_to_print: Sequence[str], end: str = "\n"):
    for line in list_to_print:
        print(line, end=end)


def format_bytes(number_of_bytes: int) -> str:
    unit = "bytes"
    bytes_float = float(number_of_bytes)
    if bytes_float / 1024 > 1:
        unit = "KB"
        bytes_float = bytes_float / 1024
    else:
        return "{} {}".format(number_of_bytes, unit)
    if bytes_float / 1024 > 1:
        unit = "MB"
        bytes_float = bytes_float / 1024
    if bytes_float / 1024 > 1:
        unit = "GB"
        bytes_float = bytes_float / 1024
    return "{:.3f} {}".format(bytes_float, unit).replace(".", ",")


def comma_separated(input_list: Sequence[str]) -> str:
    return ",".join(input_list)


def split_by_tab(input_str: str) -> Sequence[str]:
    result: list[str] = []
    for part in input_str.strip().split("\t"):
        # Remove empty strings, if two tabs are following each other
        if part:
            result.append(part)
    return result
