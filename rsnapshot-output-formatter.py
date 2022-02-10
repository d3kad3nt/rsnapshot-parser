#!/usr/bin/env python3

import argparse
import os
from datetime import datetime

UTF_8 = "UTF-8"


def getArgparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="This program is used to format the output of rsnapshot and output it to different backends"
    )
    parser.add_argument("-o", "--output", nargs="+", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument(
        "-c", "--configfile", required=False, help="The used Rsnapshot configfile"
    )
    return parser


def findLinesStartingWith(lines, key):
    return [m for m in lines if m.startswith(key)]


def printList(list, end="\n"):
    for line in list:
        print(line, end=end)


class RsnapshotCommand:
    def addLog(self, log):
        self.log = log

    def backupStartLine(self):
        return ""

    # def __str__(self):
    # 	return "{} (Type: {}), Log Lines: {}".format(self.command, self.type, len(self.log))


class BackupExecCommand(RsnapshotCommand):
    def __init__(self, command):
        self.command = command

    def backupStartLine(self):
        return self.command


class BackupScriptCommand(RsnapshotCommand):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def backupStartLine(self):
        return self.source


class BackupCommand(RsnapshotCommand):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def backupStartLine(self):
        return "{} /mnt/Backup/daily.0/{}".format(self.source, self.destination)

    def getChangedSize(self):
        if self.type is not BackupType.Backup:
            return -1
        print(self.type)
        print(self.command)
        printList(self.log)
        changedStr = (
            findLinesStartingWith(self.log, "Total bytes received")[0]
            .split(":")[1]
            .strip()
        )
        changed = Int(changedStr)
        print(changedStr)
        print(changed)
        return changed


class LogOutput:
    def __init__(self, config, input):
        self.config = config
        self.log = self.readInput(input)
        self.backupPoints = self.parseBackupPoints()

    def parseBackupPoints(self):
        backupPoints = self.config.getBackupPoints()
        currentBackupPoint = 0
        currentBackupPointLog = []
        for line in self.log:
            if backupPoints[currentBackupPoint].backupStartLine() in line:
                if currentBackupPoint > 0:
                    backupPoints[currentBackupPoint - 1].addLog(currentBackupPointLog)
                currentBackupPoint += 1
                currentBackupPointLog = []
            currentBackupPointLog.append(line)
        backupPoints[currentBackupPoint].addLog(currentBackupPointLog)
        return backupPoints

    def readInput(self, filename: str):
        with open(filename, "r", encoding="utf8") as logfile:
            lines = logfile.readlines()
        linestart = ""
        reallines = []
        for line in lines:
            # Rsnapshot cuts long lines into multiple lines seperated by "\"
            if linestart:
                line = linestart + line[4:]
                # print("combined line: {}".format(line))
            if line.endswith("\\\n"):
                linestart = line.strip()[:-1]
                # print("half-line: {}".format(linestart))
            else:
                linestart = ""
                reallines.append(line)
        return reallines

    def executedBackupCommands(self):
        executedCommands = 0
        for backupPoint in self.backupPoints:
            if hasattr(backupPoint, "log") and len(backupPoint.log) > 0:
                executedCommands += 1
        return executedCommands

    def notExecutedBackupCommands(self):
        notExecutedCommands = 0
        for backupPoint in self.backupPoints:
            if hasattr(backupPoint, "log") and len(backupPoint.log) == 0:
                notExecutedCommands += 1
        return notExecutedCommands

    def failedBackupCommands(self):
        failedCommands = 0
        for backupPoint in self.backupPoints:
            if hasattr(backupPoint, "failed") and backupPoint.failed:
                failedCommands += 1
        return failedCommands


class RsnapshotConfig:
    def __init__(self, argparse):
        self.parseConfig(argparse)

    def getValuesInConfig(self, key):
        return list(
            map(
                lambda line: line.strip().split("\t")[1],
                findLinesStartingWith(self.lines, key),
            )
        )

    def getSnapshotRoot(self):
        return self.getValuesInConfig("snapshot_root")[0]

    def getBackupPoints(self):
        backupPoints = []
        for line in self.lines:
            if line.startswith("backup\t"):
                command = line.strip().split("\t")
                backupPoints.append(BackupCommand(command[1], command[2]))
            elif line.startswith("backup_script"):
                command = line.strip().split("\t")
                backupPoints.append(BackupScriptCommand(command[1], command[2]))
            elif line.startswith("backup_exec"):
                command = line.strip().split("\t")
                backupPoints.append(BackupExecCommand(command[1]))
        return backupPoints

    def parseConfig(self, args):
        configfile = ""
        if args.configfile:
            configfile = args.configfile
            if not os.path.isfile(configfile):
                raise Exception("The configfile {} doesn't exist.".format(configfile))
        else:
            configfile = "/etc/rsnapshot.conf"
        with open(configfile, "r", encoding=UTF_8) as config:
            configLines = self.loadConfig(config)
            self.lines = configLines

    def loadConfig(self, configfile):
        result = []
        for line in configfile:
            if line.startswith("#"):
                continue
            elif "include_conf" in line:
                command = line.split("\t")[1].replace("`", "")
                out = subprocess.check_output(
                    command.split(), shell=True, encoding=encoding
                )
                result += self.loadConfig(out.split("\n"))
            else:
                strippedLine = line.strip()
                if strippedLine:
                    result.append(strippedLine)
        return result


class OutputModule:
    def output(self, logOutput):
        raise Exception("Not implemented in specific Module")


class TextModule(OutputModule):
    def output(self, logOutput):
        print("Backup at {}".format(datetime.now()))
        print("{} Backup Commands executed".format(logOutput.executedBackupCommands()))
        print("{} Backup Commands failed".format(logOutput.failedBackupCommands()))
        print(
            "{} Backup Commands not executed".format(
                logOutput.notExecutedBackupCommands()
            )
        )


def moduleExits(moduleName):
    # TODO add read modules
    if moduleName == "text":
        return True
    else:
        return False


def getModule(moduleName):
    return TextModule()


def outputLog(outputModuleNames, logOutput: LogOutput):
    for moduleName in outputModuleNames:
        if moduleExits(moduleName):
            getModule(moduleName).output(logOutput)


def main():
    argparser = getArgparser()
    args = argparser.parse_args()
    config = RsnapshotConfig(args)
    parsedLog = LogOutput(config, args.input)
    outputLog(args.output, parsedLog)


if __name__ == "__main__":
    main()
