import sys
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
        self._cached_start_time = None
        self._rsnapshot_config: RsnapshotConfig = config
        self._config: Config = Config(section="parser")
        self._log: Sequence[str] = self._read_input()
        self._empty_log = False
        self._backupPoints: Sequence[RsnapshotCommand] = self._parse_backup_points()

    def _parse_backup_points(self) -> Sequence[RsnapshotCommand]:
        # If the log file is empty
        if len(self._log) == 0:
            self._empty_log = True
            return []

        backup_points: Sequence[RsnapshotCommand] = self._rsnapshot_config.backup_points
        current_backup_point: int = -1
        current_backup_point_log: list[str] = []
        for line in self._log:
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
                        backup_points[i - 1].end_time = time
                    if i < (len(backup_points) - 1):
                        backup_points[i + 1].start_time = time
                    # Set also time for date command
                    backupPoint.start_time = time
                    backupPoint.end_time = time
        return backup_points

    @property
    def empty_log(self) -> bool:
        return self._empty_log

    @property
    def log(self) -> Sequence[str]:
        return self.log

    @property
    def backup_points(self) -> Sequence[RsnapshotCommand]:
        return self._backupPoints

    @property
    def start_time(self) -> datetime:
        start_time_str = ""
        try:
            time_format = "%H:%M"
            start_time_str = self._config.get_str(key="start_{}".format(self.retain_type))
            start_time: datetime = datetime.strptime(start_time_str, time_format)
            return datetime.combine(self._backupPoints[0].start_time.date(), start_time.time())
        except ValueError:
            #If the time could not be parsed, or the retaintype doesn't exist
            print("ERROR: Can't parse time {} from retain type {}".format(start_time_str, self.retain_type))
            if not self._cached_start_time:
                self._cached_start_time: datetime = datetime.now()
            return self._cached_start_time

    @property
    def end_time(self) -> datetime:
        if self.empty_log:
            return self.start_time
        return self._backupPoints[-1].end_time

    @property
    def duration(self) -> timedelta:
        delta: timedelta = self.end_time - self.start_time
        return delta - timedelta(microseconds=delta.microseconds)

    @property
    def duration_copy(self) -> timedelta:
        if self.empty_log:
            return timedelta(0)
        return self._backupPoints[0].start_time - self.start_time

    @property
    def duration_backup(self) -> timedelta:
        if self.empty_log:
            return timedelta(0)
        return self.end_time - self._backupPoints[0].start_time

    @property
    def retain_type(self) -> str:
        if self.empty_log:
            return "UNKNOWN"
        all_types: Sequence[str] = self._rsnapshot_config.retain_types
        first_move: str = utils.utils.find_first_line_starting_with(self._log, "mv")
        part = first_move.split(" ")[1].split("/")[-2].split(".")[0]
        if part not in all_types:
            print("ERROR: detected retain type {}, but configured are only {}.".format(part, all_types), file=sys.stderr)
        return part

    @property
    def changed_files(self) -> int:
        changed_files = 0
        for backupPoint in self._backupPoints:
            if isinstance(backupPoint, BackupCommand):
                changed_files += backupPoint.changed_files
        return changed_files

    @property
    def changed_size(self) -> int:
        changed_files = 0
        for backupPoint in self._backupPoints:
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
        for backupPoint in self._backupPoints:
            if isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    def commands_not_with_state_count(self, state: Type[ResultState]) -> int:
        return len(self.commands_not_with_state(state))

    def commands_not_with_state(self, state: Type[ResultState]) -> Sequence[RsnapshotCommand]:
        result: list[RsnapshotCommand] = []
        for backupPoint in self._backupPoints:
            if not isinstance(backupPoint.state, state):
                result.append(backupPoint)
        return result

    @property
    def successful(self) -> bool:
        if self.empty_log:
            return False
        return self.commands_with_state_count(FailedState) == 0 \
            and self.commands_with_state_count(NotExecutedState) == 0
