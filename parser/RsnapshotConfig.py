import subprocess
import os
from collections.abc import Iterable, Collection

from parser.Commands import BackupCommand, BackupScriptCommand, BackupExecCommand, RsnapshotCommand
from utils.utils import findLinesStartingWith


class RsnapshotConfig:
    def __init__(self, custom_configfile, encoding="UTF-8"):
        self.encoding = encoding
        self.parseConfig(custom_configfile)

    def getValuesInConfig(self, key):
        return list(
            map(
                lambda line: line.strip().split("\t")[1],
                findLinesStartingWith(self.lines, key),
            )
        )

    @property
    def snapshot_root(self):
        return self.getValuesInConfig("snapshot_root")[0]

    @property
    def backup_points(self) -> list[RsnapshotCommand]:
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

    @property
    def retain_types(self):
        types = []
        for line in self.lines:
            if line.startswith("retain"):
                types.append(line.strip().split("\t")[1])
        return types

    def parseConfig(self, custom_configfile):
        configfile = ""
        if custom_configfile:
            configfile = custom_configfile
            if not os.path.isfile(configfile):
                raise Exception("The configfile {} doesn't exist.".format(configfile))
        else:
            configfile = "/etc/rsnapshot.conf"
        with open(configfile, "r", encoding=self.encoding) as config:
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
                    command.split(), shell=True, encoding=self.encoding
                )
                result += self.loadConfig(out.split("\n"))
            else:
                strippedLine = line.strip()
                if strippedLine:
                    result.append(strippedLine)
        return result
