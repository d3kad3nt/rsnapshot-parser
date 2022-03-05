import datetime
from collections.abc import Sequence
from typing import Optional

from parser.ResultStates import *
from utils.utils import find_first_line_starting_with


class RsnapshotCommand:
    def __init__(self):
        self.log: Sequence[str] = []
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

    def backup_start_line(self, retain_type: Optional[str]) -> str:
        return ""

    @property
    def state(self) -> ResultState:
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        return UnknownState("Not implemented")


class BackupExecCommand(RsnapshotCommand):
    def __init__(self, command: str):
        self.command: str = command
        super().__init__()

    def backup_start_line(self, _: Optional[str]) -> str:
        return self.command

    def __str__(self):
        return "Backup Exec: {}".format(self.command)


class BackupScriptCommand(RsnapshotCommand):
    def __init__(self, source: str, destination: str):
        self.source: str = source
        self.destination: str = destination
        super().__init__()

    def backup_start_line(self, _: Optional[str]) -> str:
        return self.source

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
            Exception("No retain type given")
        return "{} /mnt/Backup/{}.0/{}".format(self.source, retain_type, self.destination)

    @property
    def total_files(self) -> int:
        changed_str: str = (
            find_first_line_starting_with(self.log, "Number of files").split(":")[1].strip().split("(")[0].strip()
        )
        changed = int(changed_str.replace(",", ""))
        return changed

    @property
    def changed_files(self) -> int:
        changed_str: str = (
            find_first_line_starting_with(self.log, "Number of regular files transferred").split(":")[1].strip()
        )
        changed = int(changed_str.replace(",", ""))
        return changed

    @property
    def total_size(self) -> int:
        changed_str: str = (
            find_first_line_starting_with(self.log, "Total file size").split(":")[1].strip().split(" ")[0].strip()
        )
        changed = int(changed_str.replace(",", ""))
        return changed

    @property
    def changed_size(self) -> int:
        changed_str: str = (
            find_first_line_starting_with(self.log, "Total bytes received").split(":")[1].strip()
        )
        changed = int(changed_str.replace(",", ""))
        return changed

    @property
    def state(self) -> ResultState:
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        if find_first_line_starting_with(self.log, "rsync succeeded"):
            return SuccessState("rsync succeeded")

        return UnknownState("Not implemented")

    @property
    def changed_file_list(self) -> Sequence[str]:
        start_changed_files = "receiving incremental file list"
        filelist = False
        files = []
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
