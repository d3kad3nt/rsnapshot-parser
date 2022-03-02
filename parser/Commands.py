import datetime

from parser.ResultStates import *
from utils.utils import find_lines_starting_with, print_list


class RsnapshotCommand:
    def __init__(self):
        self.log = []
        self._start_time: datetime.datetime = datetime.datetime.min
        self._end_time: datetime.datetime = datetime.datetime.min

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: datetime.datetime):
        self._start_time = start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self._start_time

    @end_time.setter
    def end_time(self, end_time: datetime.datetime):
        self._end_time = end_time

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        self._log = log

    def backup_start_line(self):
        return ""

    @property
    def state(self):
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        return UnknownState("Not implemented")


class BackupExecCommand(RsnapshotCommand):
    def __init__(self, command):
        self.command: str = command
        super().__init__()

    def backup_start_line(self):
        return self.command

    def __str__(self):
        return "Backup Exec: {}".format(self.command)


class BackupScriptCommand(RsnapshotCommand):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        super().__init__()

    def backup_start_line(self):
        return self.source

    def state(self):
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        return UnknownState("No way found to check state")

    def __str__(self):
        return "Backup Script: Command: {}, Dest: {}".format(
            self.source, self.destination
        )


class BackupCommand(RsnapshotCommand):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        super().__init__()

    def backup_start_line(self):
        return "{} /mnt/Backup/daily.0/{}".format(self.source, self.destination)

    @property
    def changed_size(self):
        print_list(self.log)
        changed_str = (
            find_lines_starting_with(self.log, "Total bytes received")[0].split(":")[1].strip()
        )
        changed = int(changed_str)
        return changed

    @property
    def state(self):
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        if find_lines_starting_with(self.log, "rsync succeeded"):
            return SuccessState("rsync succeeded")

        return UnknownState("Not implemented")

    @property
    def get_changed_files(self):
        start_changed_files = "receiving incremental file list"
        filelist = False
        files = []
        for line in self.log:
            if start_changed_files in line:
                filelist = True
            elif line.strip().is_empty():
                filelist = False
            elif filelist:
                files.append(line.strip())
        return files

    def __str__(self):
        return "Backup: Source: {}, Dest: {}".format(self.source, self.destination)
