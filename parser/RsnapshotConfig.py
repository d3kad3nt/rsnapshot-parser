import os
import subprocess

from parser.Commands import BackupCommand, BackupScriptCommand, BackupExecCommand, RsnapshotCommand
from utils.utils import find_lines_starting_with


class RsnapshotConfig:
    def __init__(self, custom_configfile, encoding="UTF-8"):
        self.encoding = encoding
        self._parse_config(custom_configfile)

    def get_values_in_config(self, key):
        return list(
            map(
                lambda line: line.strip().split("\t")[1],
                find_lines_starting_with(self.lines, key),
            )
        )

    @property
    def snapshot_root(self):
        return self.get_values_in_config("snapshot_root")[0]

    @property
    def backup_points(self) -> list[RsnapshotCommand]:
        backup_points = []
        for line in self.lines:
            if line.startswith("backup\t"):
                command = line.strip().split("\t")
                backup_points.append(BackupCommand(command[1], command[2]))
            elif line.startswith("backup_script"):
                command = line.strip().split("\t")
                backup_points.append(BackupScriptCommand(command[1], command[2]))
            elif line.startswith("backup_exec"):
                command = line.strip().split("\t")
                backup_points.append(BackupExecCommand(command[1]))
        return backup_points

    @property
    def retain_types(self):
        return self.get_values_in_config("retain")

    def _parse_config(self, custom_configfile):
        if custom_configfile:
            configfile = custom_configfile
            if not os.path.isfile(configfile):
                raise Exception("The configfile {} doesn't exist.".format(configfile))
        else:
            configfile = "/etc/rsnapshot.conf"
        with open(configfile, "r", encoding=self.encoding) as config:
            config_lines = self._load_config(config)
            self.lines = config_lines

    def _load_config(self, configfile):
        result = []
        for line in configfile:
            if line.startswith("#"):
                continue
            elif "include_conf" in line:
                command = line.split("\t")[1].replace("`", "")
                out = subprocess.check_output(
                    command.split(), shell=True, encoding=self.encoding
                )
                result += self._load_config(out.split("\n"))
            else:
                stripped_line = line.strip()
                if stripped_line:
                    result.append(stripped_line)
        return result
