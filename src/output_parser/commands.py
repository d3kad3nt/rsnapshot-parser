import datetime
from collections.abc import Sequence
from typing import Optional

from output_parser.result_states import (
    FailedState,
    NotExecutedState,
    ResultState,
    SuccessState,
    UnknownState,
)
from utils.utils import find_first_line_starting_with


class RsnapshotCommand:
    def __init__(self):
        self._log: Sequence[str] = []
        self._start_time: datetime.datetime = datetime.datetime.min
        self._end_time: datetime.datetime = datetime.datetime.min
        self._errormessage: str = ""

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: datetime.datetime):
        self._start_time = start_time

    @property
    def errormessage(self) -> str:
        return self._errormessage

    @property
    def end_time(self) -> datetime.datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime.datetime):
        self._end_time = end_time

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_time - self.start_time

    @property
    def log(self) -> Sequence[str]:
        return self._log

    @log.setter
    def log(self, log: Sequence[str]):
        self._log = log

    # pylint: disable=unused-argument
    def backup_start_line(self, retain_type: Optional[str]) -> str:
        return ""

    @property
    def state(self) -> ResultState:
        if self.errormessage:
            return FailedState(self.errormessage)
        if len(self._log) == 0:
            return NotExecutedState("The Command was not executed")
        return UnknownState("Not implemented")


class BackupExecCommand(RsnapshotCommand):
    def __init__(self, command: str):
        self.command: str = command
        super().__init__()

    def backup_start_line(self, retain_type: Optional[str]) -> str:
        return self.command

    def __str__(self):
        return "Backup Exec: {}".format(self.command)

    @property
    def errormessage(self) -> str:
        warning_log = find_first_line_starting_with(self.log, "WARNING")
        if warning_log:
            warning_str = warning_log.split(":")[1].strip()
            if find_first_line_starting_with(self.log, "ssh:"):
                return find_first_line_starting_with(self.log, "ssh:").strip()
            else:
                return warning_str
        return ""


class BackupScriptCommand(RsnapshotCommand):
    def __init__(self, source: str, destination: str):
        self.source: str = source
        self.destination: str = destination
        super().__init__()

    def backup_start_line(self, retain_type: Optional[str]) -> str:
        return self.source

    @property
    def state(self) -> ResultState:
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        return UnknownState("No way found to check state")

    def __str__(self):
        return "Backup Script: Command: {}, Dest: {}".format(
            self.source, self.destination
        )


class BackupCommand(RsnapshotCommand):
    def __init__(self, source: str, destination: str):
        self.source: str = source
        self.destination: str = destination
        super().__init__()

    def backup_start_line(self, retain_type: Optional[str]) -> str:
        if not retain_type:
            raise Exception("No retain type given")
        return "{} /mnt/Backup/{}.0/{}".format(
            self.source, retain_type, self.destination
        )

    @property
    def errormessage(self) -> str:
        error_line = find_first_line_starting_with(self.log, "rsync error")
        if error_line:
            rsync_message: str = error_line.split(":")[1].strip()
            if find_first_line_starting_with(self.log, "WARNING:"):
                return (
                    find_first_line_starting_with(self.log, "WARNING:")
                    .split(":", maxsplit=1)[1]
                    .strip()
                )
            elif rsync_message.startswith("unexplained error"):
                if find_first_line_starting_with(self.log, "ssh:"):
                    return find_first_line_starting_with(self.log, "ssh:")
                else:
                    return rsync_message
            else:
                return rsync_message
        return ""

    @property
    def total_files(self) -> int:
        log_line = find_first_line_starting_with(self.log, "Number of files")
        total_files: int
        if log_line:
            total_files_str: str = log_line.split(":")[1].strip().split("(")[0].strip()
            total_files = int(total_files_str.replace(",", ""))
        else:
            total_files = 0
        return total_files

    @property
    def changed_files(self) -> int:
        log_line: str = find_first_line_starting_with(
            self.log, "Number of regular files transferred"
        )
        changed: int
        if log_line:
            changed_str: str = log_line.split(":")[1].strip()
            changed = int(changed_str.replace(",", ""))
        else:
            changed = 0
        return changed

    @property
    def total_size(self) -> int:
        log_line = find_first_line_starting_with(self.log, "Total file size")
        total_size: int
        if log_line:
            total_size_str: str = log_line.split(":")[1].strip().split(" ")[0].strip()
            total_size = int(total_size_str.replace(",", ""))
        else:
            total_size = 0
        return total_size

    @property
    def changed_size(self) -> int:
        log_line = find_first_line_starting_with(self.log, "Total bytes received")
        changed: int
        if log_line:
            changed_str: str = log_line.split(":")[1].strip()
            changed = int(changed_str.replace(",", ""))
        else:
            changed = 0
        return changed

    @property
    def state(self) -> ResultState:
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        if self.errormessage:
            return FailedState(self.errormessage)
        if find_first_line_starting_with(self.log, "rsync succeeded"):
            return SuccessState("rsync succeeded")
        return UnknownState("Not implemented")

    @property
    def changed_file_list(self) -> Sequence[str]:
        start_changed_files = "receiving incremental file list"
        filelist = False
        files: list[str] = []
        for line in self.log:
            if start_changed_files in line:
                filelist = True
            elif line.strip():
                filelist = False
            elif filelist:
                files.append(line.strip())
        return files

    def __str__(self):
        return "Backup: Source: {}, Dest: {}".format(self.source, self.destination)
