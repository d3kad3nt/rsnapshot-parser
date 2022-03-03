#!/usr/bin/env python3

import argparse
from collections.abc import Sequence

from modules.modules import get_output_module
from modules.outputModule import OutputModule
from parser.ParsedOutput import ParsedOutput
from parser.RsnapshotConfig import RsnapshotConfig

UTF_8 = "UTF-8"


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="This program is used to format the output of rsnapshot and output it to different backends"
    )
    parser.add_argument("-o", "--output", nargs="+", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument(
        "-c", "--configfile", required=False, help="The used Rsnapshot configfile"
    )
    return parser.parse_args()


def output_log(output_module_names: Sequence[str], parsed_output: ParsedOutput) -> None:
    for moduleName in output_module_names:
        module: OutputModule = get_output_module(moduleName)
        module.output(parsed_output)


def main() -> None:
    args: argparse.Namespace = get_args()
    config: RsnapshotConfig = RsnapshotConfig(args.configfile)
    parsed_log: ParsedOutput = ParsedOutput(config=config, rsnapshot_output_file= args.input)
    output_log(output_module_names=args.output, parsed_output=parsed_log)


if __name__ == "__main__":
    main()
