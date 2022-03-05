import os
import subprocess
import sys
from collections.abc import Sequence
from typing import TextIO, Union

from parser.Commands import BackupCommand, BackupScriptCommand, BackupExecCommand, RsnapshotCommand
from utils.config import Config
from utils.utils import find_lines_starting_with, find_first_line_starting_with, split_by_tab


class RsnapshotConfig:
    def __init__(self, encoding: str = "UTF-8"):
        self.encoding: str = encoding
        self._config = Config(section="parser")
        self._parse_config()
        self._check_verbose_level()

    def _get_values_in_config(self, key: str) -> Sequence[str]:
        return list(
            map(
                lambda line: split_by_tab(line)[1],
                find_lines_starting_with(self.lines, key),
            )
        )

    def _get_first_value_in_config(self, key: str) -> str:
        return split_by_tab(find_first_line_starting_with(self.lines, key))[1].strip()

    @property
    def snapshot_root(self) -> str:
        return self._get_first_value_in_config("snapshot_root")

    @property
    def backup_points(self) -> Sequence[RsnapshotCommand]:
        backup_points: list[RsnapshotCommand] = []
        for line in self.lines:
            if line.startswith("backup\t"):
                command = split_by_tab(line)
                backup_points.append(BackupCommand(command[1], command[2]))
            elif line.startswith("backup_script"):
                command = split_by_tab(line)
                backup_points.append(BackupScriptCommand(command[1], command[2]))
            elif line.startswith("backup_exec"):
                command = split_by_tab(line)
                backup_points.append(BackupExecCommand(command[1]))
        return backup_points

    @property
    def retain_types(self) -> Sequence[str]:
        return self._get_values_in_config("retain")

    @property
    def lines(self) -> Sequence[str]:
        return self._lines

    @property
    def verbose_level(self) -> int:
        return int(self._get_first_value_in_config("verbose"))

    def _parse_config(self) -> None:
        configfile: str = self._config.get_value(key="rsnapshot_config", default_value="/etc/rsnapshot.conf")
        if not os.path.isfile(configfile):
            raise Exception("The configfile {} doesn't exist.".format(configfile))

        with open(configfile, "r", encoding=self.encoding) as config:
            self._lines: Sequence[str] = self._load_config(config)

    def _load_config(self, configfile: Union[TextIO, Sequence[str]]) -> Sequence[str]:
        result: list[str] = []
        for line in configfile:
            if line.startswith("#"):
                continue
            elif "include_conf" in line:
                command: str = split_by_tab(line)[1].replace("`", "")
                out: str = subprocess.check_output(
                    command.split(), shell=True, encoding=self.encoding
                )
                result += self._load_config(out.split("\n"))
            else:
                stripped_line: str = line.strip()
                if stripped_line:
                    result.append(stripped_line)
        return result

    def _check_verbose_level(self):
        if self.verbose_level < 5:
            print("The verbose level of Rsnapshot has to be 5.", file=sys.stderr)
