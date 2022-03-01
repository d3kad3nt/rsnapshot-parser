from parser.ResultStates import *
from utils.utils import findLinesStartingWith, printList


class RsnapshotCommand:
    def __init__(self):
        self.log = []

    def addLog(self, log):
        self.log = log
        self.state = self.getState()

    def backupStartLine(self):
        return ""

    def getState(self):
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        return UnknownState("Not implemented")


class BackupExecCommand(RsnapshotCommand):
    def __init__(self, command):
        self.command = command
        super().__init__()

    def backupStartLine(self):
        return self.command

    def __str__(self):
        return "Backup Exec: {}".format(self.command)


class BackupScriptCommand(RsnapshotCommand):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        super().__init__()

    def backupStartLine(self):
        return self.source

    def getState(self):
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

    def addLog(self, log):
        self.log = log

    def backupStartLine(self):
        return "{} /mnt/Backup/daily.0/{}".format(self.source, self.destination)

    def getChangedSize(self):
        print(self.type)
        print(self.command)
        printList(self.log)
        changedStr = (
            findLinesStartingWith(self.log, "Total bytes received")[0]
            .split(":")[1]
            .strip()
        )
        changed = int(changedStr)
        print(changedStr)
        print(changed)
        return changed

    def getState(self):
        if len(self.log) == 0:
            return NotExecutedState("The Command was not executed")
        if findLinesStartingWith(self.log, "rsync succeeded"):
            return SuccessState("rsync succeeded")

        return UnknownState("Not implemented")

    def __str__(self):
        return "Backup: Source: {}, Dest: {}".format(self.source, self.destination)
