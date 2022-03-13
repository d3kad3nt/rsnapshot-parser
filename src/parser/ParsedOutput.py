from collections.abc import Sequence
from typing import Type

import utils.utils
from parser.Commands import RsnapshotCommand, BackupExecCommand, BackupCommand
from parser.ResultStates import FailedState, NotExecutedState, ResultState
from parser.RsnapshotConfig import RsnapshotConfig
from utils.config import Config
from datetime import datetime, timedelta
from sys import stdin


class ParsedOutput:
    def __init__(self, config: RsnapshotConfig):
        self.rsnapshot_config: RsnapshotConfig = config
        self.config: Config = Config(section="parser")
        self.log: Sequence[str] = self._read_input()
        self.backupPoints: Sequence[RsnapshotCommand] = self._parse_backup_points()
        self.end_time: datetime = self.backupPoints[-1].end_time

    def _parse_backup_points(self) -> Sequence[RsnapshotCommand]:
        backup_points: Sequence[RsnapshotCommand] = self.rsnapshot_config.backup_points
        current_backup_point: int = -1
        current_backup_point_log: list[str] = []
        for line in self.log:
            if (current_backup_point + 1) < len(backup_points) \
                    and backup_points[current_backup_point + 1].backup_start_line(self.retain_type) in line:
                if current_backup_point >= 0:
                    backup_points[current_backup_point].log = current_backup_point_log
                current_backup_point += 1
                current_backup_point_log = []
            current_backup_point_log.append(line)
        backup_points[current_backup_point].log = current_backup_point_log
        for i, backupPoint in enumerate(backup_points):
            if isinstance(backupPoint, BackupExecCommand):
                if backupPoint.command.startswith("/bin/date"):
                    time: datetime = datetime.fromtimestamp(int(backupPoint.log[1]))
                    if i > 1:
                        backup_points[i-1].end_time = time
                    if i < (len(backup_points) - 1):
                        backup_points[i+1].start_time = time
                    #Set also time for date command
                    backupPoint.start_time = time
                    backupPoint.end_time = time
        return backup_points

    @property
    def start_time(self) -> datetime:
        time_format = "%H:%M"
        start_time_str = self.config.get_str(key="start_{}".format(self.retain_type))
        start_time: datetime = datetime.strptime(start_time_str, time_format)
        return datetime.combine(self.backupPoints[0].start_time.date(), start_time.time())

    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time

    @property
    def duration_copy(self) -> timedelta:
        return self.backupPoints[0].start_time - self.start_time

    @property
    def duration_backup(self) -> timedelta:
        return self.end_time - self.backupPoints[0].start_time

    @property
    def retain_type(self) -> str:
        all_types: Sequence[str] = self.rsnapshot_config.retain_types
        first_move: str = utils.utils.find_first_line_starting_with(self.log, "mv")
        part = first_move.split(" ")[1].split("/")[-2].split(".")[0]
        if part not in all_types:
            print("ERROR: detected retain type {}, but configured are only {}.".format(part, all_types))
        return part

    @property
    def changed_files(self) -> int:
        changed_files = 0
        for backupPoint in self.backupPoints:
            if isinstance(backupPoint, BackupCommand):
                changed_files += backupPoint.changed_files
        return changed_files

    @property
    def changed_size(self) -> int:
        changed_files = 0
        for backupPoint in self.backupPoints:
            if isinstance(backupPoint, BackupCommand):
                changed_files += backupPoint.changed_files
        return changed_files

    @staticmethod
    def _read_input() -> Sequence[str]:
        multiline_segment: str = ""
        processed_lines: list[str] = []
        for line in stdin:
            # Rsnapshot cuts long lines into multiple lines seperated by "\"
            if multiline_segment:
                line = multiline_segment + line[4:]
            if line.endswith("\\\n"):
                multiline_segment = line.strip()[:-1]
            else:
                multiline_segment = ""
                processed_lines.append(line)
        return processed_lines

    def commands_with_state_count(self, state: Type[ResultState]) -> int:
        return len(self.commands_with_state(state))

    def commands_with_state(self, state: Type[ResultState]) -> Sequence[RsnapshotCommand]:
        result: list[RsnapshotCommand] = []
        for backupPoint in self.backupPoints:
            if isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    def commands_not_with_state_count(self, state: Type[ResultState]) -> int:
        return len(self.commands_not_with_state(state))

    def commands_not_with_state(self, state: Type[ResultState]) -> Sequence[RsnapshotCommand]:
        result: list[RsnapshotCommand] = []
        for backupPoint in self.backupPoints:
            if not isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    @property
    def successful(self) -> bool:
        return self.commands_with_state_count(FailedState) == 0 \
               and self.commands_with_state_count(NotExecutedState) == 0
