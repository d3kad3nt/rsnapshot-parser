#!/usr/bin/env python3

import argparse
import glob
import os

import modules.modules
from modules import *
from parser.ParsedOutput import LogOutput
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


class Mock:
    pass


def getArgsMock():
    args = Mock()
    args.output = ["text", "test"]
    args.configfile = "rsnapshot.conf"
    args.input = "rsnapshot.out"
    return args

def getModule(moduleName):
    return modules.all_modules[moduleName]


def moduleExits(moduleName):
    curr_path = os.path.join(os.path.dirname(__file__), "modules")
    moduleFiles = []
    for f in glob.glob("{}/*.py".format(curr_path)):
        moduleFiles.append(os.path.basename(f).split(".")[0])
    moduleFiles.remove("__init__")
    return moduleName in moduleFiles


def outputLog(outputModuleNames, logOutput: LogOutput):
    for moduleName in outputModuleNames:
        if moduleExits(moduleName):
            getModule(moduleName).output(logOutput)


def main():
    args = getArgsMock()
    config = RsnapshotConfig(args.configfile)
    parsedLog = LogOutput(config, args.input)
    outputLog(args.output, parsedLog)


if __name__ == "__main__":
    main()
