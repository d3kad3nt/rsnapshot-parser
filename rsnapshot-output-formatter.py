#!/usr/bin/env python3

import argparse
import glob
import os

import modules.modules
from modules import *
from parser.ParsedOutput import ParsedOutput
from parser.RsnapshotConfig import RsnapshotConfig

UTF_8 = "UTF-8"


def getArgs():
    parser = argparse.ArgumentParser(
        description="This program is used to format the output of rsnapshot and output it to different backends"
    )
    parser.add_argument("-o", "--output", nargs="+", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument(
        "-c", "--configfile", required=False, help="The used Rsnapshot configfile"
    )
    return parser.parse_args()


def getModule(moduleName):
    return modules.all_modules[moduleName]


def moduleExits(module_name: str):
    return module_name.lower() in modules.all_modules


def outputLog(outputModuleNames, logOutput: ParsedOutput):
    for moduleName in outputModuleNames:
        if moduleExits(moduleName):
            getModule(moduleName.lower()).output(logOutput)
        else:
            print("Module {} not found".format(moduleName))


def main():
    args = getArgs()
    config = RsnapshotConfig(args.configfile)
    parsed_log = ParsedOutput(config, args.input)
    outputLog(args.output, parsed_log)


if __name__ == "__main__":
    main()
