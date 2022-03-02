#!/usr/bin/env python3

import argparse

import modules.modules
from modules import *
from modules.outputModule import OutputModule
from parser.ParsedOutput import ParsedOutput
from parser.RsnapshotConfig import RsnapshotConfig

UTF_8 = "UTF-8"


def get_args():
    parser = argparse.ArgumentParser(
        description="This program is used to format the output of rsnapshot and output it to different backends"
    )
    parser.add_argument("-o", "--output", nargs="+", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument(
        "-c", "--configfile", required=False, help="The used Rsnapshot configfile"
    )
    return parser.parse_args()


def output_log(output_module_names: list[str], parsed_output: ParsedOutput):
    for moduleName in output_module_names:
        module: OutputModule = modules.get_module(moduleName)
        module.output(parsed_output)


def main():
    args = get_args()
    config = RsnapshotConfig(args.configfile)
    parsed_log = ParsedOutput(config, args.input)
    output_log(args.output, parsed_log)


if __name__ == "__main__":
    main()
